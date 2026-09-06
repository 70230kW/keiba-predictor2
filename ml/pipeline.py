"""Offline common-CSV importer. No network calls; no vendor data redistribution."""
import argparse
import csv
import json
import math
from datetime import date
from pathlib import Path

SCHEMA = json.loads(Path(__file__).with_name("schema.json").read_text())
FEATURES = SCHEMA["features"]
METADATA = SCHEMA["metadata"]
RAW = SCHEMA["raw"]


def exact_columns(actual, expected):
    if len(actual) != len(set(actual)):
        raise ValueError("Duplicate column names")
    missing, extra = set(expected) - set(actual), set(actual) - set(expected)
    if missing or extra:
        raise ValueError(f"Invalid columns: missing={sorted(missing)}, forbidden/unknown={sorted(extra)}")


def number(value, name, low, high, integer=False):
    try:
        result = float(value)
    except (ValueError, TypeError):
        raise ValueError(f"{name}: numeric value required") from None
    if not math.isfinite(result) or not low <= result <= high or (integer and not result.is_integer()):
        raise ValueError(f"{name}: invalid range or non-integer value")
    return int(result) if integer else result


def load_results(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        exact_columns(reader.fieldnames or [], RAW)
        rows, seen, race_conditions, horse_dates = [], set(), {}, set()
        for line, row in enumerate(reader, 2):
            try:
                if None in row or any(value is None or not value.strip() for value in row.values()):
                    raise ValueError("Missing values or malformed CSV")
                row = {key: value.strip() for key, value in row.items()}
                row["race_date"] = date.fromisoformat(row["race_date"]).isoformat()
                for key in ("race_id", "horse_id"):
                    if not row[key].isascii() or not all(c.isalnum() or c in "_-" for c in row[key]):
                        raise ValueError(f"{key}: use ASCII letters, digits, underscores or hyphens")
                row["distance_m"] = number(row["distance_m"], "distance_m", 400, 5000, True)
                row["carried_weight"] = number(row["carried_weight"], "carried_weight", 30, 80)
                row["age"] = number(row["age"], "age", 2, 20, True)
                row["finish_position"] = number(row["finish_position"], "finish_position", 1, 18, True)
                identity = (row["race_id"], row["horse_id"])
                if identity in seen:
                    raise ValueError("Duplicate horse in race")
                horse_day = (row["horse_id"], row["race_date"])
                if horse_day in horse_dates:
                    raise ValueError("Multiple starts for the same horse on the same date")
                conditions = (row["race_date"], row["distance_m"])
                if row["race_id"] in race_conditions and race_conditions[row["race_id"]] != conditions:
                    raise ValueError("Conflicting race date/distance")
                seen.add(identity)
                horse_dates.add(horse_day)
                race_conditions[row["race_id"]] = conditions
                rows.append(row)
            except ValueError as exc:
                raise ValueError(f"CSV line {line}: {exc}") from exc
    if not rows:
        raise ValueError("Empty CSV")
    return sorted(rows, key=lambda row: (row["race_date"], row["race_id"], row["horse_id"]))


def build_features(rows):
    histories, output = {}, []
    for row in sorted(rows, key=lambda item: (item["race_date"], item["race_id"], item["horse_id"])):
        history = histories.get(row["horse_id"], [])
        day = date.fromisoformat(row["race_date"])
        prior = [item for item in history if item[0] < day]
        result = {key: row[key] for key in ("race_date", "race_id", "horse_id", "distance_m", "carried_weight", "age")}
        result.update(
            finished_first=int(row["finish_position"] == 1),
            prior_starts=len(prior),
            prior_win_rate=sum(position == 1 for _, position in prior) / len(prior) if prior else 0,
            prior_mean_finish=sum(position for _, position in prior) / len(prior) if prior else 0,
            days_since_last=(day - prior[-1][0]).days if prior else 0,
        )
        output.append(result)
        histories.setdefault(row["horse_id"], []).append((day, row["finish_position"]))
    return output


def temporal_split(rows):
    days = sorted({row["race_date"] for row in rows})
    if len(days) < 3:
        raise ValueError("At least three distinct race dates are required")
    validation_start = min(len(days) - 2, max(1, int(len(days) * .6)))
    test_start = min(len(days) - 1, max(validation_start + 1, int(len(days) * .8)))
    return (
        [r for r in rows if r["race_date"] < days[validation_start]],
        [r for r in rows if days[validation_start] <= r["race_date"] < days[test_start]],
        [r for r in rows if r["race_date"] >= days[test_start]],
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, default=Path("data/processed/training.csv"))
    args = parser.parse_args()
    rows = build_features(load_results(args.input))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation protects previous datasets from accidental overwrite.
    with args.output.open("x", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=METADATA + FEATURES)
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps({"rows": len(rows), "races": len({r["race_id"] for r in rows}), "output": str(args.output)}))


if __name__ == "__main__":
    main()

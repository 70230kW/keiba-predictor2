import csv
import tempfile
import unittest
from pathlib import Path
from ml.pipeline import RAW, build_features, exact_columns, load_results, temporal_split


class PipelineTests(unittest.TestCase):
    def fixture(self, extra=None):
        rows = []
        for month in range(1, 6):
            for horse, place in (("A", 1), ("B", 2)):
                rows.append(dict(zip(RAW, [f"2025-{month:02d}-01", f"r{month}", horse, "1800", "56", "4", str(place)])))
        if extra:
            extra(rows)
        return rows

    def read(self, rows):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.csv"
            with path.open("w", encoding="utf-8-sig", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
            return load_results(path)

    def test_prior_only(self):
        rows = self.read(self.fixture())
        first = build_features(rows)
        self.assertEqual(first[0]["prior_starts"], 0)
        self.assertEqual(first[2]["prior_starts"], 1)
        rows[-2]["finish_position"] = 8
        self.assertEqual(first[:-2], build_features(rows)[:-2])
        self.assertEqual(first[-2]["prior_win_rate"], build_features(rows)[-2]["prior_win_rate"])

    def test_date_groups_do_not_overlap(self):
        parts = temporal_split(build_features(self.read(self.fixture())))
        for left, right in zip(parts, parts[1:]):
            self.assertLess(max(r["race_date"] for r in left), min(r["race_date"] for r in right))
            self.assertFalse({r["race_id"] for r in left} & {r["race_id"] for r in right})

    def test_market_and_unknown_columns_rejected(self):
        for key in ("odds", "past_odds", "人気", "sns_score", "finish_position"):
            with self.assertRaises(ValueError):
                exact_columns(["distance_m", key], ["distance_m"])

    def test_duplicate_rejected(self):
        rows = self.fixture()
        rows.append(rows[0].copy())
        with self.assertRaises(ValueError):
            self.read(rows)

    def test_nan_rejected(self):
        with self.assertRaises(ValueError):
            self.read(self.fixture(lambda rows: rows[0].update(carried_weight="NaN")))

    def test_conflicting_race_rejected(self):
        with self.assertRaises(ValueError):
            self.read(self.fixture(lambda rows: rows[1].update(distance_m="2000")))

    def test_missing_rejected(self):
        with self.assertRaises(ValueError):
            self.read(self.fixture(lambda rows: rows[0].update(age="")))

    def test_short_history_rejected(self):
        with self.assertRaises(ValueError):
            temporal_split(build_features(self.read(self.fixture())[:2]))


if __name__ == "__main__":
    unittest.main()

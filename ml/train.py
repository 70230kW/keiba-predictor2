"""Train from strictly validated, past-only features produced by ml.pipeline."""
from pathlib import Path
import argparse
import json
from .pipeline import FEATURES, METADATA, exact_columns, temporal_split


def train(csv_path: Path, output_path: Path) -> None:
    import joblib
    import lightgbm as lgb
    import pandas as pd
    from sklearn.metrics import brier_score_loss, log_loss

    if output_path.exists() or output_path.with_suffix(".metrics.json").exists():
        raise ValueError("Output already exists; choose a new model path")
    frame = pd.read_csv(csv_path, dtype={"race_id": str, "horse_id": str})
    exact_columns(list(frame.columns), METADATA + FEATURES)
    if frame.empty or frame.isna().any().any():
        raise ValueError("Empty dataset or missing values")
    frame["race_date"] = pd.to_datetime(frame["race_date"], format="%Y-%m-%d", errors="raise").dt.strftime("%Y-%m-%d")
    if frame.duplicated(["race_id", "horse_id"]).any():
        raise ValueError("Duplicate race/horse")
    if (frame.groupby("race_id")["race_date"].nunique() != 1).any():
        raise ValueError("Conflicting dates for the same race")
    for column in FEATURES:
        frame[column] = pd.to_numeric(frame[column], errors="raise")
        if not frame[column].map(lambda value: float("-inf") < value < float("inf")).all():
            raise ValueError(f"Non-finite feature: {column}")
    if not frame["finished_first"].isin([0, 1]).all():
        raise ValueError("Target must be binary")
    parts = [pd.DataFrame(rows) for rows in temporal_split(frame.to_dict("records"))]
    for part in parts:
        if part["finished_first"].nunique() != 2:
            raise ValueError("Every partition requires both winning and non-winning examples")
    training, validation, testing = parts
    model = lgb.LGBMClassifier(n_estimators=500, learning_rate=.03, num_leaves=31, random_state=42, verbosity=-1, n_jobs=2)
    model.fit(training[FEATURES], training["finished_first"],
              eval_set=[(validation[FEATURES], validation["finished_first"])],
              callbacks=[lgb.early_stopping(50)])
    probabilities = model.predict_proba(testing[FEATURES])[:, 1]
    baseline = [float(training["finished_first"].mean())] * len(testing)
    metrics = {
        "test_rows": len(testing),
        "test_races": int(testing["race_id"].nunique()),
        "log_loss": float(log_loss(testing["finished_first"], probabilities, labels=[0, 1])),
        "brier_score": float(brier_score_loss(testing["finished_first"], probabilities)),
        "baseline_log_loss": float(log_loss(testing["finished_first"], baseline, labels=[0, 1])),
        "partitions": [{"rows": len(part), "from": part["race_date"].min(), "to": part["race_date"].max()} for part in parts],
        "warning": "Uncalibrated binary probabilities; not race-normalized. Not for live wagering.",
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("xb") as stream:
        joblib.dump({"model": model, "features": FEATURES, "schema_version": 2}, stream)
    with output_path.with_suffix(".metrics.json").open("x", encoding="utf-8") as stream:
        json.dump(metrics, stream, ensure_ascii=False, indent=2)
    print(json.dumps(metrics, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("data/processed/training.csv"))
    parser.add_argument("--output", type=Path, default=Path("artifacts/baseline.joblib"))
    arguments = parser.parse_args()
    train(arguments.input, arguments.output)

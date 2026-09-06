"""Time-aware baseline trainer. Odds and popularity are intentionally forbidden."""
from pathlib import Path
import joblib
import lightgbm as lgb
import pandas as pd

FORBIDDEN = {"odds","win_odds","place_odds","final_odds","popularity","bet_share","payout","tip_mark"}
TARGET, DATE = "finished_first", "race_date"

def validate_features(columns: list[str]) -> None:
    normalized = {column.strip().lower() for column in columns}
    violations = sorted(feature for feature in FORBIDDEN if feature in normalized)
    if violations:
        raise ValueError(f"Forbidden prediction features: {', '.join(violations)}")

def train(csv_path: Path, output_path: Path) -> None:
    frame = pd.read_csv(csv_path, parse_dates=[DATE]).sort_values(DATE)
    features = [column for column in frame.columns if column not in {TARGET, DATE, "race_id", "horse_id"}]
    validate_features(features)
    split = int(len(frame) * 0.8)
    train_frame, validation_frame = frame.iloc[:split], frame.iloc[split:]
    model = lgb.LGBMClassifier(n_estimators=500, learning_rate=0.03, num_leaves=31, random_state=42)
    model.fit(train_frame[features], train_frame[TARGET], eval_set=[(validation_frame[features], validation_frame[TARGET])], callbacks=[lgb.early_stopping(50)])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": model, "features": features}, output_path)

if __name__ == "__main__":
    train(Path("data/processed/training.csv"), Path("artifacts/baseline.joblib"))

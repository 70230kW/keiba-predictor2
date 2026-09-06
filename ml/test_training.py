"""Synthetic integration test: verifies plumbing, not real predictive accuracy."""
import csv
import json
import tempfile
import unittest
from pathlib import Path
from ml.pipeline import METADATA, FEATURES, build_features, load_results
from ml.test_pipeline import PipelineTests
from ml.train import train


class TrainingTests(unittest.TestCase):
    def test_import_train_evaluate(self):
        fixture = PipelineTests()
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            raw = folder / "results.csv"
            rows = fixture.fixture()
            with raw.open("w", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
            prepared = folder / "training.csv"
            with prepared.open("w", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=METADATA + FEATURES)
                writer.writeheader()
                writer.writerows(build_features(load_results(raw)))
            model = folder / "model.joblib"
            train(prepared, model)
            self.assertTrue(model.exists())
            metrics = json.loads(model.with_suffix(".metrics.json").read_text())
            self.assertEqual(metrics["test_races"], 1)
            self.assertGreaterEqual(metrics["log_loss"], 0)
            with self.assertRaises(ValueError):
                train(prepared, model)

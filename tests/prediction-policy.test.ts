import assert from "node:assert/strict";
import test from "node:test";
import { assertObjectiveFeatures } from "../lib/prediction-policy.ts";
test("許可された客観的データ", () => assert.doesNotThrow(() => assertObjectiveFeatures(["distance_m", "prior_win_rate"])));
test("市場データ・未知列・当該結果は拒否", () => {
  for (const column of ["odds", "previous_odds", "popularity", "人気", "sns_score", "finished_first", "finish_position"]) {
    assert.throws(() => assertObjectiveFeatures(["distance_m", column]), /予測禁止データ/);
  }
});
test("重複列は拒否", () => assert.throws(() => assertObjectiveFeatures(["distance_m", "distance_m"])));

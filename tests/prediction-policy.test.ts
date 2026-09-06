import assert from "node:assert/strict";
import test from "node:test";
import { assertObjectiveFeatures } from "../lib/prediction-policy.ts";
test("客観的な競走データを許可する",()=>assert.doesNotThrow(()=>assertObjectiveFeatures(["last_3f","course_fit","horse_weight"])));
test("オッズや人気を拒否する",()=>assert.throws(()=>assertObjectiveFeatures(["last_3f","win_odds","popularity"]),/予測禁止データ/));

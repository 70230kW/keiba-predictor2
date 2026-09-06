export const FORBIDDEN_PREDICTION_FEATURES = ["odds","win_odds","place_odds","final_odds","popularity","bet_share","payout","tip_mark"] as const;

export function assertObjectiveFeatures(featureNames: readonly string[]): void {
  const normalized = featureNames.map((name) => name.trim().toLowerCase());
  const violations = FORBIDDEN_PREDICTION_FEATURES.filter((feature) =>
    normalized.some((name) => name === feature || name.startsWith(`${feature}_`)),
  );
  if (violations.length > 0) throw new Error(`予測禁止データが含まれています: ${violations.join(", ")}`);
}

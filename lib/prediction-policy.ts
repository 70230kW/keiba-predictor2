import schema from "../ml/schema.json" with { type: "json" };

// Fail closed: market-derived aliases AND unknown/result columns are rejected.
export function assertObjectiveFeatures(featureNames: readonly string[]): void {
  const violations = featureNames.filter((name) => !schema.features.includes(name));
  if (new Set(featureNames).size !== featureNames.length || violations.length > 0) {
    throw new Error(`予測禁止データまたは不明な特徴量: ${violations.join(", ")}`);
  }
}

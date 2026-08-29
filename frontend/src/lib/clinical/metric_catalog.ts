/**
 * ApexCare Clinical Calculation Registry & Interactive Score Engines
 */

export interface ClinicalMetricDefinition {
  metricCode: string;
  title: string;
  category: string;
  minScore: number;
  maxScore: number;
  criticalThreshold: number;
}

export function buildClinicalMetricsCatalog(): ClinicalMetricDefinition[] {
  const records: ClinicalMetricDefinition[] = [];
  const cats = ["Critical Care", "Cardiovascular", "Neurology", "Pediatrics", "Emergency Trauma", "Gastroenterology", "Nephrology", "Pulmonology"];
  cats.forEach((cat, catI) => {
    for (let mI = 1; mI <= 55; mI++) {
      const metricCode = `METRIC-${String(catI).padStart(2, "0")}-${String(mI).padStart(3, "0")}`;
      const title = `${cat} Scoring Assessment Engine #${mI}`;
      records.push({ metricCode, title, category: cat, minScore: 0, maxScore: 100, criticalThreshold: 75 });
      for (let s = 1; s <= 3; s++) {
        records.push({ metricCode: `${metricCode}-S${s}`, title: `${title} (Sub-scale ${s})`, category: cat, minScore: 0, maxScore: 100, criticalThreshold: 75 });
      }
    }
  });
  return records;
}

export const CLINICAL_METRICS_CATALOG: ClinicalMetricDefinition[] = buildClinicalMetricsCatalog();

export function getClinicalMetric(code: string): ClinicalMetricDefinition | undefined {
  return CLINICAL_METRICS_CATALOG.find((m) => m.metricCode === code);
}

/**
 * ApexCare Frontend Clinical Pathology Reference Intervals
 */

export interface LabCatalogItem {
  testCode: string;
  testName: string;
  discipline: string;
  units: string;
  refLow: number;
  refHigh: number;
  isPanicSensitive: boolean;
}

export function buildLabCatalogRegistry(): LabCatalogItem[] {
  const records: LabCatalogItem[] = [];
  const disciplines = ["HEMATOLOGY", "BIOCHEMISTRY", "IMMUNOLOGY", "MICROBIOLOGY", "ENDOCRINOLOGY", "TOXICOLOGY"];
  disciplines.forEach((disc) => {
    for (let a = 1; a <= 45; a++) {
      const testCode = `LAB-${disc.slice(0, 3)}-${String(a).padStart(3, "0")}`;
      const testName = `${disc} Diagnostic Assay #${a}`;
      const refLow = 1.0 + a * 0.4;
      const refHigh = refLow + 10.0 + a * 0.8;
      const isPanic = a % 4 === 0;
      records.push({ testCode, testName, discipline: disc, units: "mg/dL", refLow, refHigh, isPanicSensitive: isPanic });
      for (let s = 1; s <= 3; s++) {
        records.push({ testCode: `${testCode}-S${s}`, testName: `${testName} Variant #${s}`, discipline: disc, units: "mg/dL", refLow, refHigh, isPanicSensitive: isPanic });
      }
    }
  });
  return records;
}

export const LAB_CATALOG_REGISTRY: LabCatalogItem[] = buildLabCatalogRegistry();

export function searchLabCatalog(query: string, limit: number = 30): LabCatalogItem[] {
  const q = query.toLowerCase().trim();
  if (!q) return LAB_CATALOG_REGISTRY.slice(0, limit);
  return LAB_CATALOG_REGISTRY.filter((t) =>
    t.testCode.toLowerCase().includes(q) || t.testName.toLowerCase().includes(q)
  ).slice(0, limit);
}

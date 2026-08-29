/**
 * ApexCare Frontend Client-Side Pharmacopeia Lookup
 */

export interface DrugRecord {
  code: string;
  genericName: string;
  brandName: string;
  therapeuticClass: string;
  standardDose: string;
  isControlled: boolean;
}

export function buildDrugRegistry(): DrugRecord[] {
  const records: DrugRecord[] = [];
  const classes = ["Cardiovascular", "Antimicrobials", "Central Nervous", "Gastrointestinal", "Endocrine", "Respiratory"];
  classes.forEach((cName, cIdx) => {
    for (let dIdx = 1; dIdx <= 40; dIdx++) {
      const code = `MED-${String(cIdx).padStart(2, "0")}-${String(dIdx).padStart(3, "0")}`;
      const gen = `${cName} Generic Molecule #${dIdx}`;
      const brd = `ApexCare-${cName.slice(0, 3)}-${dIdx}`;
      const isCtrl = dIdx % 8 === 0;
      records.push({ code, genericName: gen, brandName: brd, therapeuticClass: cName, standardDose: `${dIdx * 10}mg PO daily`, isControlled: isCtrl });
      for (let v = 1; v <= 3; v++) {
        records.push({ code: `${code}-V${v}`, genericName: gen, brandName: `${brd} XR #${v}`, therapeuticClass: cName, standardDose: `${dIdx * 10 * v}mg Specialized Dose`, isControlled: isCtrl });
      }
    }
  });
  return records;
}

export const DRUG_REGISTRY: DrugRecord[] = buildDrugRegistry();

export function searchDrugs(query: string, limit: number = 30): DrugRecord[] {
  const q = query.toLowerCase().trim();
  if (!q) return DRUG_REGISTRY.slice(0, limit);
  return DRUG_REGISTRY.filter((d) =>
    d.genericName.toLowerCase().includes(q) || d.brandName.toLowerCase().includes(q) || d.code.toLowerCase().includes(q)
  ).slice(0, limit);
}

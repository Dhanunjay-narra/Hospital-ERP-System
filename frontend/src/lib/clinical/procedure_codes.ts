/**
 * ApexCare Frontend Clinical Procedure & Surgical Fee Matrix
 */

export interface ProcedureFeeItem {
  code: string;
  title: string;
  department: string;
  standardFee: number;
  rvuPoints: number;
}

export function buildProcedureRegistry(): ProcedureFeeItem[] {
  const records: ProcedureFeeItem[] = [];
  const depts = ["Cardiology", "Orthopedics", "Neurosurgery", "General Surgery", "Pediatrics", "Ophthalmology", "ENT", "Urology"];
  depts.forEach((dep, depI) => {
    for (let pI = 1; pI <= 40; pI++) {
      const code = `PRC-${dep.slice(0, 3).toUpperCase()}-${String(pI).padStart(3, "0")}`;
      const title = `${dep} Specialized Intervention #${pI}`;
      const standardFee = 500 + depI * 200 + pI * 45;
      const rvuPoints = 1.5 + pI * 0.3;
      records.push({ code, title, department: dep, standardFee, rvuPoints });
      for (let v = 1; v <= 3; v++) {
        records.push({ code: `${code}-T${v}`, title: `${title} Tier ${v}`, department: dep, standardFee: standardFee + v * 150, rvuPoints: rvuPoints + v * 0.5 });
      }
    }
  });
  return records;
}

export const PROCEDURE_REGISTRY: ProcedureFeeItem[] = buildProcedureRegistry();

export function searchProcedures(query: string, limit: number = 30): ProcedureFeeItem[] {
  const q = query.toLowerCase().trim();
  if (!q) return PROCEDURE_REGISTRY.slice(0, limit);
  return PROCEDURE_REGISTRY.filter((p) =>
    p.code.toLowerCase().includes(q) || p.title.toLowerCase().includes(q)
  ).slice(0, limit);
}

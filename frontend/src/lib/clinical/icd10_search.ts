/**
 * ApexCare Frontend Client-Side ICD-10 Diagnostic Index
 */

export interface ICD10Record {
  code: string;
  description: string;
  chapter: string;
  isChronic: boolean;
  severityWeight: number;
}

export function buildICD10Registry(): ICD10Record[] {
  const records: ICD10Record[] = [];
  const chapters = [
    ["Certain infectious and parasitic diseases", "A00-B99"],
    ["Neoplasms", "C00-D49"],
    ["Diseases of the blood", "D50-D89"],
    ["Endocrine and metabolic diseases", "E00-E89"],
    ["Mental and behavioral disorders", "F01-F99"],
    ["Diseases of the nervous system", "G00-G99"],
    ["Diseases of the eye and adnexa", "H00-H59"],
    ["Diseases of the ear and mastoid", "H60-H95"],
    ["Diseases of the circulatory system", "I00-I99"],
    ["Diseases of the respiratory system", "J00-J99"],
    ["Diseases of the digestive system", "K00-K95"],
    ["Diseases of the musculoskeletal system", "M00-M99"],
  ];

  chapters.forEach(([chName], chIdx) => {
    for (let itemIdx = 1; itemIdx <= 35; itemIdx++) {
      const code = `C${String(chIdx).padStart(2, "0")}.${String(itemIdx).padStart(2, "0")}`;
      const desc = `${chName} - Specifier #${itemIdx}`;
      const isChronic = itemIdx % 2 === 0;
      records.push({ code, description: desc, chapter: chName, isChronic, severityWeight: 1.0 + itemIdx * 0.05 });
      for (let s = 1; s <= 3; s++) {
        records.push({ code: `${code}.${s}`, description: `${desc} (Subtype ${s})`, chapter: chName, isChronic, severityWeight: 1.0 + itemIdx * 0.05 + s * 0.1 });
      }
    }
  });
  return records;
}

export const ICD10_REGISTRY: ICD10Record[] = buildICD10Registry();

export function searchICD10(query: string, limit: number = 30): ICD10Record[] {
  const q = query.toLowerCase().trim();
  if (!q) return ICD10_REGISTRY.slice(0, limit);
  return ICD10_REGISTRY.filter((item) =>
    item.code.toLowerCase().includes(q) || item.description.toLowerCase().includes(q)
  ).slice(0, limit);
}

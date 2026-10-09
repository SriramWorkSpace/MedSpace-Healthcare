/**
 * Normalizes an answer before rendering. The model sometimes cites as 【2】 or 【2†L3-L5】 and
 * groups as [1, 2]; the server rewrites new answers, and this keeps older saved ones readable.
 */
export function normalizeAnswer(text) {
  return text
    .replace(/【/g, "[")
    .replace(/】/g, "]")
    .replace(/\[(\d{1,2})†[^\]]*\]/g, "[$1]")
    .replace(/\[(\d{1,2}(?:\s*,\s*\d{1,2})+)\]/g, (_, group) =>
      group
        .split(/\s*,\s*/)
        .map((n) => `[${n}]`)
        .join(""),
    );
}

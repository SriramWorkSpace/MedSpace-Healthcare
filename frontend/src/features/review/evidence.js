/**
 * Evidence highlights (ADR-031): map a review-form field to where it is printed on the page.
 *
 * The API keys evidence by the extraction's original positions ("medications.2.strength").
 * Items can be removed or added while reviewing, so each item carries `_ev`, its original
 * position, and lookups go through it rather than the current index.
 */

const COLLECTION = /^(medications|care_actions|diet_notes|lab_results)\.(\d+)(?:\.(.+))?$/;

/** { field, item } evidence keys for a form path, or null for an item the reader didn't find. */
export function evidenceKeys(path, getValues) {
  const m = COLLECTION.exec(path ?? "");
  if (!m) {
    const top = path.split(".")[0];
    return { field: path, item: top === "prescriber" ? "prescriber" : null };
  }
  const original = getValues(`${m[1]}.${m[2]}._ev`);
  if (!original) return null;
  return { field: m[3] ? `${original}.${m[3].split(".")[0]}` : null, item: original };
}

/** The most specific spot: the field itself, else its whole item (a medicine line, a lab row). */
export function findSpot(evidence, keys) {
  if (!evidence || !keys) return null;
  return evidence.fields?.[keys.field] ?? evidence.items?.[keys.item] ?? null;
}

/** A short human name for the item a form path belongs to ("Metformin", "HbA1c"). */
export function itemName(path, getValues) {
  const m = COLLECTION.exec(path ?? "");
  if (!m) return "";
  const item = getValues(`${m[1]}.${m[2]}`) ?? {};
  return item.name || item.title || item.text || "";
}

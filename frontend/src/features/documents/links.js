/**
 * Link from a record to where it came from: the document, on its page, with the item
 * highlighted when the record knows which line it was read from (ADR-031).
 */
export function sourceLink({ document_id, source_page, source_ref }) {
  const qs = new URLSearchParams();
  if (source_page) qs.set("page", String(source_page));
  if (source_ref) qs.set("show", source_ref);
  return `/app/documents/${document_id}${qs.size ? `?${qs}` : ""}`;
}

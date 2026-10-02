/** "Follow-up with Dr. Imani Oduya" -> "Dr. Imani Oduya" (appointment titles from the timeline). */
export function clinicianFrom(title) {
  const m = /\bwith\s+(.+)$/i.exec(title ?? "");
  return m ? m[1].trim() : null;
}

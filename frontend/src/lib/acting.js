/**
 * Whose records this tab is showing (ADR-026). Null means the signed-in user's own.
 *
 * Kept in sessionStorage so it is per tab and ends with the tab: a caregiver never "wakes up"
 * inside someone else's records. The API client sends it as X-Acting-For; the server decides
 * what is allowed.
 */
const KEY = "ms-acting";
let acting = read();
const listeners = new Set();

function read() {
  try {
    return JSON.parse(sessionStorage.getItem(KEY) ?? "null");
  } catch {
    return null;
  }
}

export const getActing = () => acting;

export function onActingChange(fn) {
  listeners.add(fn);
  return () => listeners.delete(fn);
}

/** `person`: { id, name, role } from the care circle, or null for your own records. */
export function setActing(person) {
  acting = person ? { id: person.id, name: person.name, role: person.role } : null;
  try {
    if (acting) sessionStorage.setItem(KEY, JSON.stringify(acting));
    else sessionStorage.removeItem(KEY);
  } catch {
    /* storage unavailable: stays in memory for this tab */
  }
  listeners.forEach((fn) => fn(acting));
}

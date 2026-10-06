import { z } from "zod";

// Never compile validators with Function(): the CSP forbids it (script-src 'self'), and Zod's
// probe for it would log a violation on every page that validates a form.
z.config({ jitless: true });

export { z };

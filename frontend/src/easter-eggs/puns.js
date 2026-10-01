/**
 * The MedSpace pun pharmacy. Dispensed in small doses: loaders, empty states, 404, footer.
 * Rule: puns never replace the information a user needs; they ride alongside it.
 */

export const LOADING_PUNS = [
  "Taking your documents' pulse",
  "Deciphering the doctor's handwriting",
  "Scrubbing in",
  "Checking vitals",
  "Running a quick check-up",
  "Consulting the chart",
  "Warming up the stethoscope",
  "Filling the prescription for data",
];

export const PROCESSING_PUNS = [
  "Reading between the lines (and the scribbles)",
  "Our AI is doing its rounds",
  "Turning cursive into clarity",
  "Extracting the good stuff, no side effects",
  "Patience is a virtue, especially for patients",
];

export const MARQUEE_PUNS = [
  "An apple a day keeps the doctor away. MedSpace keeps the paperwork away.",
  "Laughter is the best medicine. Still, follow your prescription.",
  "We take your records seriously. Our puns, less so.",
  "No appointment needed for your own data.",
  "Doctor's handwriting? We've seen worse. Well, not much worse.",
  "Your documents, finally in good health.",
];

export const EMPTY_QUIPS = {
  documents: "Clean bill of health on the paperwork front.",
  medications: "Nothing on the schedule. Your pill organizer is on vacation.",
  timeline: "A blank chart. Every story starts somewhere.",
  shares: "No links out in the wild. Privacy, prescribed.",
  chat: "Ask away. Unlike a waiting room, there's no queue.",
  review: "Inbox zero, clinically speaking.",
};

export const NOT_FOUND_LINES = [
  "This page skipped its appointment.",
  "We checked for a pulse. Nothing.",
  "This page has been discharged.",
];

export function pick(list, seed) {
  if (seed === undefined) return list[Math.floor(Math.random() * list.length)];
  return list[Math.abs(seed) % list.length];
}

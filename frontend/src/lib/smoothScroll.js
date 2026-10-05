/**
 * Quick, smooth in-page scrolling to an element, honouring its `scroll-margin-top`.
 *
 * Native `behavior: "smooth"` varies by browser and gets slow over long distances; this keeps
 * every jump between ~320 and 650 ms with an ease-in-out curve (movement on screen), runs on
 * requestAnimationFrame, stops the moment the user scrolls, touches or presses a key, and is
 * instant when reduced motion is requested.
 */
const easeInOutCubic = (t) => (t < 0.5 ? 4 * t * t * t : 1 - (-2 * t + 2) ** 3 / 2);

let cancelCurrent = null;

/** `onDone(completed)`: true when it arrived, false when the user interrupted. */
export function smoothScrollTo(el, { onDone } = {}) {
  cancelCurrent?.();
  const margin = parseFloat(getComputedStyle(el).scrollMarginTop) || 0;
  const start = window.scrollY;
  const max = document.documentElement.scrollHeight - window.innerHeight;
  const target = Math.min(max, Math.max(0, el.getBoundingClientRect().top + start - margin));
  const distance = target - start;
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (reduce || Math.abs(distance) < 2) {
    window.scrollTo(0, target);
    onDone?.(true);
    return;
  }

  const duration = Math.min(650, 320 + Math.abs(distance) * 0.12);
  let frame = 0;
  let begin = null;
  const stop = (completed = false) => {
    cancelAnimationFrame(frame);
    for (const type of ["wheel", "touchstart", "keydown", "pointerdown"]) {
      window.removeEventListener(type, interrupt, true);
    }
    if (cancelCurrent === stop) cancelCurrent = null;
    onDone?.(completed);
  };
  const interrupt = () => stop(); // the user took over: never fight them
  for (const type of ["wheel", "touchstart", "keydown", "pointerdown"]) {
    window.addEventListener(type, interrupt, { capture: true, passive: true });
  }
  cancelCurrent = stop;

  const step = (now) => {
    begin ??= now;
    const t = Math.min(1, (now - begin) / duration);
    window.scrollTo(0, start + distance * easeInOutCubic(t));
    if (t < 1) frame = requestAnimationFrame(step);
    else stop(true);
  };
  frame = requestAnimationFrame(step);
}

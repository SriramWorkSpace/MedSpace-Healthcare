// Renders public/favicon.svg into the PNG icons the web app manifest needs.
//   node scripts/icons.mjs
import { mkdirSync, readFileSync } from "node:fs";
import { chromium } from "@playwright/test";

const svg = readFileSync("public/favicon.svg", "utf8");
mkdirSync("public/icons", { recursive: true });
const browser = await chromium.launch();
const page = await browser.newPage();

// "any": the logo fills the square. "maskable": logo inside the 80% safe zone on brand green,
// so launchers can crop it to a circle or squircle without clipping the cross.
const variants = [
  ["icon-192.png", 192, 1],
  ["icon-512.png", 512, 1],
  ["icon-maskable-512.png", 512, 0.62],
  ["apple-touch-icon.png", 180, 0.78],
];
for (const [name, size, scale] of variants) {
  const inner = Math.round(size * scale);
  await page.setViewportSize({ width: size, height: size });
  await page.setContent(
    `<body style="margin:0;width:${size}px;height:${size}px;display:grid;place-items:center;background:${scale < 1 ? "#1f7a5c" : "transparent"}">
       <div style="width:${inner}px;height:${inner}px">${svg.replace("<svg ", `<svg width="${inner}" height="${inner}" `)}</div>
     </body>`,
  );
  await page.screenshot({ path: `public/icons/${name}`, omitBackground: scale === 1 });
}
await browser.close();
console.log("icons written to public/icons");

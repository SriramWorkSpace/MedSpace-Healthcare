// Renders the logo mark (public/brand/logo-mark-512.png) into the PNG icons the web app manifest needs.
//   node scripts/icons.mjs
import { mkdirSync, readFileSync } from "node:fs";
import { chromium } from "@playwright/test";

const mark = `data:image/png;base64,${readFileSync("public/brand/logo-mark-512.png").toString("base64")}`;
mkdirSync("public/icons", { recursive: true });
const browser = await chromium.launch();
const page = await browser.newPage();

// "any": the logo fills the square. "maskable": logo inside the 80% safe zone on white,
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
    `<body style="margin:0;width:${size}px;height:${size}px;display:grid;place-items:center;background:${scale < 1 ? "#ffffff" : "transparent"}">
       <img src="${mark}" width="${inner}" height="${inner}" />
     </body>`,
  );
  await page.screenshot({ path: `public/icons/${name}`, omitBackground: scale === 1 });
}
await browser.close();
console.log("icons written to public/icons");

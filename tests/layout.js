// Layout checks for wrapped figures, run in a browser on a rendered fixture.
// Serve tests/ over HTTP, open a fixture's HTML, then run in the console:
//   const m = await import("/layout.js"); m.report()
// report() returns one entry per wrapped figure, per wrap group that has a
// block after it, and per image inside a wrapped float, each with `ok` and
// the measured values.

const TOL = 1; // px

const wrapped = () => [
  ...document.querySelectorAll(
    ".quarto-float.wrap-left, .quarto-float.wrap-right, .wrapped-image.wrap-left, .wrapped-image.wrap-right"
  ),
];

const sideOf = (el) => (el.classList.contains("wrap-left") ? "left" : "right");

const near = (a, b) => Math.abs(a - b) <= TOL;

// Resolves a CSS length such as "35%", "3in", or "1em" to px, measured as
// a width inside `parent`.
function resolve(value, parent) {
  const probe = document.createElement("div");
  probe.style.width = value;
  probe.style.height = "0";
  probe.style.visibility = "hidden";
  parent.appendChild(probe);
  const px = probe.getBoundingClientRect().width;
  probe.remove();
  return px;
}

// The box of the first line of the first paragraph after a wrapped figure.
function firstLine(group) {
  const p = group.querySelector(":scope > p");
  if (!p) return null;
  const walker = document.createTreeWalker(p, NodeFilter.SHOW_TEXT);
  let node = walker.nextNode();
  while (node && !node.textContent.trim()) node = walker.nextNode();
  if (!node) return null;
  const start = node.textContent.search(/\S/);
  const range = document.createRange();
  range.setStart(node, start);
  range.setEnd(node, start + 1);
  return range.getBoundingClientRect();
}

function figureEntry(el) {
  const side = sideOf(el);
  const cs = getComputedStyle(el);
  const box = el.getBoundingClientRect();
  const group = el.closest(".wrap-group");
  const column = group ? group.getBoundingClientRect().width : NaN;
  const entry = { id: el.id || el.querySelector("img")?.getAttribute("src"), side, float: cs.float };
  if (cs.float === "none") {
    entry.ok = false;
    return entry;
  }
  const style = el.style;
  const width = style.getPropertyValue("--wrap-width").trim();
  const gap = style.getPropertyValue("--wrap-gap").trim();
  entry.width = { set: width, expected: +resolve(width, group).toFixed(1), measured: +box.width.toFixed(1), column: +column.toFixed(1) };
  // The computed margin is in layout px, and the boxes are in screen px. A
  // revealjs slide is scaled, so the margin is scaled to screen px too.
  const scale = el.offsetWidth ? box.width / el.offsetWidth : 1;
  const margin = +(parseFloat(side === "right" ? cs.marginLeft : cs.marginRight) * scale).toFixed(1);
  // A percent margin resolves against the containing block, the group.
  entry.gap = { set: gap, expected: +resolve(gap, group).toFixed(1), measured: margin };
  const line = firstLine(group);
  entry.firstLine = line ? { x: Math.round(line.left), y: Math.round(line.top) } : null;
  entry.box = { left: Math.round(box.left), top: Math.round(box.top), right: Math.round(box.right), bottom: Math.round(box.bottom) };
  const beside =
    line !== null &&
    line.top >= box.top - TOL &&
    line.top < box.bottom &&
    (side === "right" ? line.right <= box.left : line.left >= box.right);
  const img = el.querySelector("img");
  const imgWidth = img ? img.getBoundingClientRect().width : NaN;
  const content = box.width - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight)
    - parseFloat(cs.borderLeftWidth) - parseFloat(cs.borderRightWidth);
  entry.image = { width: +imgWidth.toFixed(1), boxContent: +content.toFixed(1) };
  const caption = el.querySelector("figcaption");
  let captionInside = true;
  if (caption) {
    const c = caption.getBoundingClientRect();
    const ccs = getComputedStyle(caption);
    // A line height of "normal" has no px value, so use 1.2 times the font size.
    const lineHeight = parseFloat(ccs.lineHeight) || 1.2 * parseFloat(ccs.fontSize);
    captionInside = c.left >= box.left - TOL && c.right <= box.right + TOL;
    entry.caption = { lines: Math.round(c.height / lineHeight), inside: captionInside };
  }
  entry.checks = {
    float: cs.float === side,
    beside,
    imageFillsBox: near(imgWidth, content),
    width: near(box.width, entry.width.expected),
    gap: near(margin, entry.gap.expected),
    captionInside,
  };
  entry.ok = Object.values(entry.checks).every(Boolean);
  return entry;
}

// The block that follows a wrap group. A group that ends its section is
// followed by the next section. In a dashboard, a group that ends its card
// body has no next block, since the next card is laid out apart from it.
function nextBlock(group) {
  const main = group.closest(".card-body") || group.closest("main") || document.body;
  const hidden = (el) => ["none", "contents"].includes(getComputedStyle(el).display) || el.tagName === "SCRIPT";
  let el = group;
  while (el && el !== main) {
    let next = el.nextElementSibling;
    while (next && hidden(next)) {
      next = next.nextElementSibling;
    }
    if (next) return next;
    el = el.parentElement;
  }
  return null;
}

function groupEntry(group) {
  const fig = group.querySelector(".wrap-left, .wrap-right");
  const next = nextBlock(group);
  if (!fig || !next) return null;
  const figBottom = fig.getBoundingClientRect().bottom;
  const nextTop = next.getBoundingClientRect().top;
  return {
    figure: fig.id || fig.querySelector("img")?.getAttribute("src"),
    next: next.tagName.toLowerCase() + (next.getAttribute("class") ? "." + next.getAttribute("class").split(" ").join(".") : ""),
    figureBottom: Math.round(figBottom),
    nextTop: Math.round(nextTop),
    ok: nextTop >= figBottom - TOL,
  };
}

function imageEntries() {
  return [...document.querySelectorAll(".quarto-float.wrap-left img, .quarto-float.wrap-right img")].map((img) => {
    const style = img.getAttribute("style") || "";
    const wrapClass = img.classList.contains("wrap-left") || img.classList.contains("wrap-right");
    const percentWidth = /width\s*:\s*[\d.]+%/.test(style);
    return { src: img.getAttribute("src"), wrapClass, percentWidth, ok: !wrapClass && !percentWidth };
  });
}

export function report() {
  return {
    viewport: innerWidth,
    figures: wrapped().map(figureEntry),
    groups: [...document.querySelectorAll(".wrap-group")].map(groupEntry).filter(Boolean),
    images: imageEntries(),
  };
}

// At a viewport below the breakpoint: the computed float of each wrapped
// figure.
export function floats() {
  return wrapped().map((el) => ({ id: el.id || el.querySelector("img")?.getAttribute("src"), float: getComputedStyle(el).float }));
}

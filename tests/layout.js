// Layout checks for wrapped figures, run in a browser on a rendered fixture.
// Serve tests/ over HTTP, open a fixture's HTML, then run in the console:
//   const m = await import("/layout.js"); m.report()
// report() returns one entry per wrapped figure, per wrap group that has a
// block after it, and per image inside a wrapped float, each with `ok` and
// the measured values.
// For the docs site's example pages, `python3 tests/docs_layout.py --html`
// runs `straddle()` on each page in headless Chromium. To run it by hand,
// serve docs/_site/ with this file in it and run the `straddle()` calls
// that `python3 tests/docs_layout.py --js` prints.

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
// followed by the next section. A group that ends its `.card-body` has no
// next block, since the next card body, in this card or another, is laid
// out apart from it.
function nextBlock(group) {
  const main = group.closest(".card-body") || group.closest("main") || document.body;
  let el = group;
  while (el && el !== main) {
    let next = el.nextElementSibling;
    while (next && (getComputedStyle(next).display === "none" || next.tagName === "SCRIPT")) {
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

// The line boxes of a paragraph, from its text's client rects. Inline code
// can sit a few px lower than the text around it, so a rect joins a line
// when its middle is inside the line's box, as `lines()` in
// tests/docs_layout.py does for PDFs.
function paragraphLines(p) {
  const range = document.createRange();
  range.selectNodeContents(p);
  const lines = [];
  const rects = [...range.getClientRects()].sort((a, b) => a.top - b.top || b.height - a.height);
  for (const r of rects) {
    if (!r.width) continue;
    const middle = (r.top + r.bottom) / 2;
    const line = lines.find((l) => l.top <= middle && middle <= l.bottom);
    if (line) {
      line.left = Math.min(line.left, r.left);
      line.right = Math.max(line.right, r.right);
      line.bottom = Math.max(line.bottom, r.bottom);
    } else {
      lines.push({ top: r.top, bottom: r.bottom, left: r.left, right: r.right });
    }
  }
  return lines.sort((a, b) => a.top - b.top);
}

// The docs pages' check that tests/docs_layout.py runs on the PDFs, which
// prints the `cases` for each page (`--js`). Each case lists words that
// appear in the paragraph before a wrapped figure (`above`) and in the
// paragraph that runs beside and below it (`straddle`), in figure order.
export function straddle(cases) {
  const figs = wrapped();
  const paras = [...document.querySelectorAll("main p")];
  const has = (p, words) => words.every((w) => p.textContent.replace(/\s+/g, " ").includes(w));
  let pos = 0;
  return cases.map((c, n) => {
    const el = figs[n];
    const box = el?.getBoundingClientRect();
    const crosses = (l) => (c.side === "right" ? l.right > box.left + TOL : l.left < box.right - TOL);
    const ai = paras.findIndex((p, i) => i >= pos && has(p, c.above));
    const si = paras.findIndex((p, i) => i > ai && has(p, c.straddle));
    const problems = [];
    if (!el || sideOf(el) !== c.side) return { figure: el?.id, ok: false, problems: ["figure missing or on the other side"] };
    if (ai < 0 || si < 0) return { figure: el.id, ok: false, problems: ["paragraph not found"] };
    pos = si + 1;
    const above = paragraphLines(paras[ai]);
    const para = paragraphLines(paras[si]);
    if (above.length < 2) problems.push(`paragraph above has ${above.length} line`);
    else if (!above.slice(0, -1).every(crosses)) problems.push("a line above does not cross the figure");
    const beside = para.filter((l) => l.bottom > box.top && l.top < box.bottom && !crosses(l));
    const below = para.filter((l) => l.top >= box.bottom - TOL && crosses(l));
    if (!beside.length) problems.push("no line of the paragraph beside the figure");
    else if (!below.some((l) => l.top > beside[0].top)) problems.push("no later line below the figure that crosses it");
    return { figure: el.id || el.querySelector("img")?.getAttribute("src"), ok: !problems.length, problems };
  });
}

// At a viewport below the breakpoint: the computed float of each wrapped
// figure.
export function floats() {
  return wrapped().map((el) => ({ id: el.id || el.querySelector("img")?.getAttribute("src"), float: getComputedStyle(el).float }));
}

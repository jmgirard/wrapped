-- wrapped: wrap body text around figures marked .wrap-left or .wrap-right.
--
-- Runs at pre-quarto, after Quarto creates FloatRefTarget nodes. HTML output
-- floats each wrapped figure inside a .wrap-group div that also holds the
-- paragraphs after it. Every other format keeps a normal figure. A figure
-- with no wrap class is left as it is in every format.

local SIDES = { ["wrap-left"] = "left", ["wrap-right"] = "right" }

local DEFAULTS = {
  width = "40%",
  gap = "1em",
  breakpoint = "576px",
}

-- The document's values, read from the `wrapped:` metadata in the first pass.
local options = {
  width = DEFAULTS.width,
  gap = DEFAULTS.gap,
  breakpoint = DEFAULTS.breakpoint,
}

local is_html = quarto.doc.is_format("html:js")
local found_wrap = false

-- CSS units that a width, gap, or breakpoint may use, in lowercase.
local UNITS = {
  px = true, pt = true, pc = true, ["in"] = true, cm = true, mm = true, q = true,
  em = true, rem = true, ex = true, ch = true, lh = true, rlh = true,
  vw = true, vh = true, vmin = true, vmax = true,
  svw = true, svh = true, lvw = true, lvh = true, dvw = true, dvh = true,
  cqw = true, cqh = true, cqi = true, cqb = true, cqmin = true, cqmax = true,
}

-- CSS functions whose result is a length, passed through as written.
local FUNCTIONS = { calc = true, min = true, max = true, clamp = true }

-- Returns the wrap class in a class list, or nil.
local function wrap_class(classes)
  for _, c in ipairs(classes or {}) do
    if SIDES[c] then return c end
  end
  return nil
end

-- Removes every wrap class from a class list, in place.
local function strip_wrap(classes)
  for i = #classes, 1, -1 do
    if SIDES[classes[i]] then classes:remove(i) end
  end
end

-- Returns the CSS length for a value, or nil when the value is not a
-- number, a percent, a number with a CSS unit, or a calc(), min(), max(),
-- or clamp() expression. A unitless number is a pixel length, as in
-- Pandoc. With `no_percent`, a percent is not a length.
local function css_length(value, no_percent)
  local s = pandoc.utils.stringify(value)
  local fn = s:match("^(%a+)%(.+%)$")
  if fn and FUNCTIONS[fn:lower()] then return s end
  local num, unit = s:match("^(%d*%.?%d+)(%a*%%?)$")
  if not num then return nil end
  if unit == "" then return num .. "px" end
  if unit == "%" then
    if no_percent then return nil end
    return s
  end
  if UNITS[unit:lower()] then return s end
  return nil
end

-- Returns the CSS length for a value, or `fallback` with a warning when the
-- value is not a length. `what` and `where` name the value in the warning.
-- A breakpoint passes `no_percent`, because a media query takes no percent.
local function checked_length(value, fallback, what, where, no_percent)
  if value == nil then return fallback end
  local length = css_length(value, no_percent)
  if length then return length end
  quarto.log.warning(string.format(
    'wrapped: %s "%s" on %s is not %s, so it is %s.',
    what, pandoc.utils.stringify(value), where,
    no_percent and "a length" or "a length or a percent", fallback))
  return fallback
end

-- The custom properties for a wrapped box, followed by any style the user
-- set on it.
local function style_for(width, gap, where, existing)
  local style = string.format("--wrap-width: %s; --wrap-gap: %s;",
    checked_length(width, options.width, "width", where),
    checked_length(gap, options.gap, "wrap-gap", where))
  if existing and existing ~= "" then style = style .. " " .. existing end
  return style
end

-- True for a Div that stands for a Quarto float in a plain walk.
local function is_float_div(div)
  return div.attributes.__quarto_custom_type == "FloatRefTarget"
end

-- Reads the first wrap class, width, and wrap-gap of the images in a list
-- of blocks, and changes nothing. The images of a subfigure belong to the
-- subfigure, not to its panel, so the walk skips nested floats.
local function image_wrap(blocks)
  local class, width, gap
  blocks:walk({
    traverse = "topdown",
    Div = function(d)
      if is_float_div(d) then return nil, false end
    end,
    Image = function(img)
      class = class or wrap_class(img.classes)
      width = width or img.attributes.width
      gap = gap or img.attributes["wrap-gap"]
    end,
  })
  return class, width, gap
end

-- Removes the wrap class and wrap-gap from each image in a wrapped figure.
-- In HTML it also removes the width, so the image fills the figure box.
-- Elsewhere the image keeps its width.
local function clean_images(blocks)
  return blocks:walk({
    Image = function(img)
      strip_wrap(img.classes)
      img.attributes["wrap-gap"] = nil
      if is_html then img.attributes.width = nil end
      return img
    end,
  })
end

-- Counts the floats (figures and tables) inside a code cell. Inside a user
-- filter, a float in a cell is a Div that Quarto marks as a FloatRefTarget,
-- and a plain walk does not call the FloatRefTarget handler.
local function count_floats(div)
  local n = 0
  div:walk({
    Div = function(d)
      if d.attributes.__quarto_custom_type == "FloatRefTarget" then n = n + 1 end
    end,
  })
  return n
end

-- Custom ids of floats whose next block is not a paragraph, from the
-- next-block pass.
local no_text = {}

-- Why a float keeps its normal layout, as "is in a list", by the float's
-- custom id. The float pass gives each such float with a wrap class a
-- normal layout and a warning.
local context_of_float = {}

-- Returns the context that a margin class names, or nil.
local function margin_context(classes)
  if classes:includes("column-margin") then return "is in the margin" end
  if classes:includes("aside") then return "is in an aside" end
  return nil
end

-- Returns the context that a block sets for the blocks inside it, or nil.
-- A code cell with `column: margin` carries the column-margin class.
local function block_context(block)
  if block.t == "BulletList" or block.t == "OrderedList" then return "is in a list" end
  if block.t ~= "Div" then return nil end
  local kind = block.attributes.__quarto_custom_type
  if kind == "Callout" then return "is in a callout" end
  if kind == "Tabset" or block.classes:includes("panel-tabset") then return "is in a tabset" end
  if block.classes:includes("columns") or block.classes:includes("column") then
    return "is in a column layout"
  end
  return margin_context(block.classes)
end

-- A context warning, printed in HTML only. Other formats print the one
-- format warning instead.
local function context_warning(subject, context)
  if is_html then
    quarto.log.warning(string.format("wrapped: %s %s, so it does not wrap.", subject, context))
  end
end

-- Removes the wrap class and wrap-gap from an image, and keeps its width.
local function drop_wrap(img)
  strip_wrap(img.classes)
  img.attributes["wrap-gap"] = nil
  return img
end

-- Records the floats in a list of blocks, subfloats included, by custom id.
local function record_floats(blocks, context)
  blocks:walk({
    Div = function(d)
      if is_float_div(d) then
        local id = d.attributes.__quarto_custom_id
        context_of_float[id] = context_of_float[id] or context
      end
    end,
  })
end

-- Records each float in a context's blocks, and gives each wrapped figure
-- or image there a normal layout with a warning. A float warns later, in
-- the float pass, where its own id is known.
local function mark_context(blocks, context)
  return blocks:walk({
    traverse = "topdown",
    Div = function(div)
      if not is_float_div(div) then return nil end
      record_floats(pandoc.Blocks({ div }), context)
      return nil, false
    end,
    Figure = function(fig)
      if not (wrap_class(fig.classes) or image_wrap(fig.content)) then return nil end
      found_wrap = true
      strip_wrap(fig.classes)
      fig.content = fig.content:walk({ Image = drop_wrap })
      context_warning(fig.identifier ~= "" and ("the figure #" .. fig.identifier)
        or "a figure with no id", context)
      return fig, false
    end,
    Image = function(img)
      if not wrap_class(img.classes) then return nil end
      found_wrap = true
      context_warning("the image " .. pandoc.utils.stringify(img.src), context)
      return drop_wrap(img)
    end,
  })
end

-- Finds the lists, callouts, column layouts, tabsets, asides, margin
-- blocks, and subfigure panels, outermost first, and marks what is inside
-- each one. A float that holds other floats is a subfigure panel.
local function find_contexts(doc)
  local function mark(block)
    if block.t == "Div" and is_float_div(block) then
      local inner = pandoc.Blocks({})
      block.content:walk({
        Div = function(d) if is_float_div(d) then inner:insert(d) end end,
      })
      if #inner > 0 then
        local id = block.attributes.__quarto_custom_id
        context_of_float[id] = context_of_float[id] or "is a subfigure panel"
        record_floats(inner, "is in a subfigure panel")
      end
      return nil
    end
    local context = block_context(block)
    if not context then return nil end
    if block.t == "Div" then
      block.content = mark_context(block.content, context)
    else
      for i, item in ipairs(block.content) do
        block.content[i] = mark_context(item, context)
      end
    end
    return block, false
  end
  doc.blocks = doc.blocks:walk({
    traverse = "topdown",
    Div = mark,
    BulletList = mark,
    OrderedList = mark,
  })
  return doc
end

local function read_meta(meta)
  local m = meta.wrapped
  if m == nil then return end
  if pandoc.utils.type(m) ~= "table" then
    quarto.log.warning(
      "wrapped: the wrapped metadata is not a map of width, gap, and breakpoint, so it is ignored.")
    return
  end
  options.width = checked_length(m.width, DEFAULTS.width, "width", "the wrapped metadata")
  options.gap = checked_length(m.gap, DEFAULTS.gap, "gap", "the wrapped metadata")
  options.breakpoint = checked_length(m.breakpoint, DEFAULTS.breakpoint, "breakpoint",
    "the wrapped metadata", true)
end

-- Custom ids of wrapped floats outside a code cell, and the anchor tokens of
-- cells whose figure wrapped, for the grouping pass.
local wrapped_ids = {}
local wrapped_cells = {}
local next_token = 0

-- The wrap class of a code cell, carried to the floats inside that cell.
-- `remaining` counts the cell's floats, figures and tables, so a cell with
-- no float carries nothing. Only figures take the class.
local carry = nil

local function cell_div(div)
  if not div.classes:includes("cell") then return nil end
  -- Each cell ends any carry left from an earlier cell.
  carry = nil
  local c = wrap_class(div.classes)
  if not c then return nil end
  strip_wrap(div.classes)
  local n = count_floats(div)
  if n == 0 and is_html then
    quarto.log.warning(
      "wrapped: a code cell with a wrap class makes no figure with a fig- label, so nothing wraps.")
  end
  if n > 0 then
    next_token = next_token + 1
    local token = tostring(next_token)
    carry = { class = c, remaining = n, token = token }
    if is_html then div.attributes["data-wrap-anchor"] = token end
  end
  return div
end

local function float_target(float)
  -- Every float of a wrapped cell uses up the carry, tables included, so
  -- the carry never reaches a float after the cell.
  local carried, token
  if carry and carry.remaining > 0 then
    carry.remaining = carry.remaining - 1
    carried, token = carry.class, carry.token
  end
  local img_class, img_width, img_gap = image_wrap(float.content)
  local class = wrap_class(float.classes) or carried or img_class
  if not class then return nil end
  found_wrap = true
  strip_wrap(float.classes)
  -- Only figures wrap. A table float keeps its normal layout, and Quarto
  -- copies a cell's classes onto a table float, so the wrap class goes.
  -- A figure in a context keeps its normal layout too.
  local node = float.__quarto_custom_node
  local custom_id = node and node.attributes and node.attributes.__quarto_custom_id
  local layout = float.attributes["layout-ncol"] or float.attributes["layout-nrow"]
    or float.attributes.layout
  local context = (float.type ~= "Figure" and "is not a figure")
    or context_of_float[custom_id or ""]
    or margin_context(float.classes)
    or (layout and "is a subfigure panel")
  -- A figure with no paragraph after it keeps a normal figure with no
  -- warning (the next-block rule).
  if context or no_text[custom_id or ""] then
    float.content = float.content:walk({ Image = drop_wrap })
    float.attributes["wrap-gap"] = nil
    if context then
      context_warning(string.format("the %s #%s",
        float.type == "Figure" and "figure" or "table", float.identifier), context)
    end
    return float
  end
  float.content = clean_images(float.content)
  if not is_html then return float end
  -- knitr writes the plot's pixel size as a unitless image width. That is
  -- not a box width, so a cell figure takes only a width with a unit.
  if carried and img_width and tostring(img_width):match("^%d+%.?%d*$") then
    img_width = nil
  end
  local width = float.attributes.width or img_width
  local gap = float.attributes["wrap-gap"] or img_gap
  float.attributes.width = nil
  float.attributes["wrap-gap"] = nil
  float.classes:insert(class)
  float.attributes.style = style_for(width, gap, "#" .. float.identifier, float.attributes.style)
  if carried then
    wrapped_cells[token] = true
  else
    -- The grouping pass sees this float as a plain Div that Quarto marks
    -- with the same custom id, so it can find the float by that id.
    if custom_id then wrapped_ids[custom_id] = true end
  end
  return float
end

-- A captioned image with no #fig- id is a Pandoc Figure, not a float.
-- Quarto drops a Figure's own classes and style in HTML, so the filter puts
-- the Figure inside a .wrapped-image box. Returning false stops the
-- traversal from visiting the Figure again inside the box.
local function figure_block(fig)
  local img_class, img_width, img_gap = image_wrap(fig.content)
  local class = wrap_class(fig.classes) or img_class
  if not class then return nil end
  found_wrap = true
  strip_wrap(fig.classes)
  fig.content = clean_images(fig.content)
  if not is_html then return fig end
  local width = fig.attributes.width or img_width
  local gap = fig.attributes["wrap-gap"] or img_gap
  fig.attributes.width = nil
  fig.attributes["wrap-gap"] = nil
  local where = fig.identifier ~= "" and ("#" .. fig.identifier) or "a figure with no id"
  local box = pandoc.Div({ fig }, pandoc.Attr("", { "wrapped-image", class },
    { style = style_for(width, gap, where, nil) }))
  return box, false
end

-- A paragraph that holds only an image with a wrap class, and no caption.
local function lone_wrapped_image(block)
  if block.t ~= "Para" then return nil end
  local img
  for _, inline in ipairs(block.content) do
    if inline.t == "Image" and not img then
      img = inline
    elseif inline.t ~= "Space" and inline.t ~= "SoftBreak" then
      return nil
    end
  end
  if img and wrap_class(img.classes) then return img end
  return nil
end

local function wrapped_image_div(img)
  local class = wrap_class(img.classes)
  strip_wrap(img.classes)
  local width = img.attributes.width
  local gap = img.attributes["wrap-gap"]
  img.attributes.width = nil
  img.attributes["wrap-gap"] = nil
  return pandoc.Div({ pandoc.Plain({ img }) }, pandoc.Attr("", { "wrapped-image", class },
    { style = style_for(width, gap, pandoc.utils.stringify(img.src), nil) }))
end

-- True when raw HTML is one comment and nothing else.
local function is_comment(text)
  local body = text:match("^%s*<!%-%-(.*)%-%->%s*$")
  return body ~= nil and not body:find("-->", 1, true)
end

-- A block that a group takes in: a paragraph that does not start a wrap of
-- its own, or a raw HTML comment, which shows nothing.
local function joins_group(block)
  if block.t == "Para" then return lone_wrapped_image(block) == nil end
  return block.t == "RawBlock" and block.format:match("html") ~= nil
    and is_comment(block.text)
end

-- True when the first block after blocks[i] that is not a comment is a
-- paragraph that joins a group.
local function text_follows(blocks, i)
  for j = i + 1, #blocks do
    if not joins_group(blocks[j]) then return false end
    if blocks[j].t == "Para" then return true end
  end
  return false
end

-- The next-block rule. A wrapped figure whose next block is not a
-- paragraph has no text to wrap, so it keeps a normal figure with no
-- warning. A float or a code cell has its floats recorded for the float
-- pass. A captioned image with no id, or an image with no caption, loses
-- its wrap class here. Runs before the float pass, on the blocks as written.
local function no_text_blocks(blocks)
  for i, b in ipairs(blocks) do
    if not text_follows(blocks, i) then
      if b.t == "Div" and (is_float_div(b) or b.classes:includes("cell")) then
        pandoc.Blocks({ b }):walk({
          Div = function(d)
            if is_float_div(d) then no_text[d.attributes.__quarto_custom_id] = true end
          end,
        })
      elseif b.t == "Figure" and (wrap_class(b.classes) or image_wrap(b.content)) then
        found_wrap = true
        strip_wrap(b.classes)
        b.content = b.content:walk({ Image = drop_wrap })
        blocks[i] = b
      elseif lone_wrapped_image(b) then
        found_wrap = true
        blocks[i] = b:walk({ Image = drop_wrap })
      end
    end
  end
  return blocks
end

-- Applies the next-block rule to every list of blocks except those inside
-- a code cell or a float, where a figure is the last block by design.
local function find_no_text(doc)
  return doc:walk({
    traverse = "topdown",
    Blocks = no_text_blocks,
    Div = function(div)
      if is_float_div(div) or div.classes:includes("cell") then return nil, false end
    end,
  })
end

-- Groups each wrapped figure with the paragraphs after it. The group stops
-- at the first block that is not a paragraph (the stop rule). The group's
-- CSS contains its float, so the stop block starts below the figure.
local function group_blocks(blocks)
  local out = pandoc.List()
  local i = 1
  while i <= #blocks do
    local b = blocks[i]
    local members
    local img = lone_wrapped_image(b)
    if img then
      found_wrap = true
      if is_html then
        members = pandoc.List({ wrapped_image_div(img) })
      else
        strip_wrap(img.classes)
      end
    elseif b.t == "Div" and b.classes:includes("wrapped-image") then
      members = pandoc.List({ b })
    elseif b.t == "Div" and b.attributes["data-wrap-anchor"] then
      -- A wrapped cell starts a group only if one of its figures wrapped.
      local token = b.attributes["data-wrap-anchor"]
      b.attributes["data-wrap-anchor"] = nil
      if wrapped_cells[token] then members = pandoc.List({ b }) end
    elseif b.t == "Div" and wrapped_ids[b.attributes.__quarto_custom_id or ""] then
      members = pandoc.List({ b })
    end
    if members then
      i = i + 1
      while i <= #blocks and joins_group(blocks[i]) do
        members:insert(blocks[i])
        i = i + 1
      end
      out:insert(pandoc.Div(members, pandoc.Attr("", { "wrap-group" })))
    else
      out:insert(b)
      i = i + 1
    end
  end
  return out
end

-- An image whose wrap class is still there after the grouping pass sits
-- where the filter cannot place a box, such as inside a link or beside
-- other content in a paragraph. It keeps a normal layout, with a warning in
-- HTML. Other formats print the one format warning instead.
local function unplaced_image(img)
  if not wrap_class(img.classes) then return nil end
  found_wrap = true
  strip_wrap(img.classes)
  if is_html then
    quarto.log.warning(string.format(
      "wrapped: the image %s is not a figure or the only content of its paragraph, so it does not wrap.",
      pandoc.utils.stringify(img.src)))
  end
  return img
end

-- A div with a wrap class that is not a figure, such as `::: {.wrap-right}`,
-- keeps a normal layout, with a warning in HTML. The filter's own
-- .wrapped-image boxes carry a wrap class on purpose.
local function unplaced_div(div)
  if not wrap_class(div.classes) or div.classes:includes("wrapped-image") then return nil end
  found_wrap = true
  strip_wrap(div.classes)
  if is_html then
    local where = div.identifier ~= "" and ("#" .. div.identifier) or "with no id"
    quarto.log.warning(string.format(
      "wrapped: the div %s is not a figure, so it does not wrap.", where))
  end
  return div
end

local function add_html_assets()
  -- No version here: `_extension.yml` holds the one version marker.
  quarto.doc.add_html_dependency({
    name = "wrapped",
    stylesheets = { "wrapped.css" },
  })
  -- A custom property cannot set a media query, so the breakpoint rule is
  -- written here from the document's value.
  quarto.doc.include_text("in-header", string.format([[
<style>
@media (max-width: %s) {
  .quarto-float.wrap-left, .quarto-float.wrap-right,
  .wrapped-image.wrap-left, .wrapped-image.wrap-right {
    float: none; width: auto; margin: 1em 0;
  }
}
</style>]], options.breakpoint))
end

local function finish(doc)
  if not found_wrap then return nil end
  if is_html then
    add_html_assets()
  else
    quarto.log.warning(string.format(
      "wrapped: %s output does not wrap figures yet, so wrapped figures render as normal figures.",
      FORMAT))
  end
  return nil
end

return {
  { Meta = read_meta },
  { Pandoc = find_contexts },
  { Pandoc = find_no_text },
  {
    traverse = "topdown",
    Div = cell_div,
    FloatRefTarget = float_target,
    Figure = figure_block,
  },
  { Blocks = group_blocks },
  { Image = unplaced_image, Div = unplaced_div },
  { Pandoc = finish },
}

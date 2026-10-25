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

-- CSS units that a width, gap, or breakpoint may use.
local UNITS = {
  px = true, pt = true, pc = true, ["in"] = true, cm = true, mm = true,
  em = true, rem = true, ex = true, ch = true, vw = true, vh = true,
}

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
-- number, a percent, or a number with a CSS unit. A unitless number is a
-- pixel length, as in Pandoc.
local function css_length(value)
  local s = pandoc.utils.stringify(value)
  local num, unit = s:match("^(%d*%.?%d+)(%a*%%?)$")
  if not num then return nil end
  if unit == "" then return num .. "px" end
  if unit == "%" or UNITS[unit] then return s end
  return nil
end

-- Returns the CSS length for a value, or `fallback` with a warning when the
-- value is not a length. `what` and `where` name the value in the warning.
local function checked_length(value, fallback, what, where)
  if value == nil then return fallback end
  local length = css_length(value)
  if length then return length end
  quarto.log.warning(string.format(
    'wrapped: %s "%s" on %s is not a length or a percent, so it is %s.',
    what, pandoc.utils.stringify(value), where, fallback))
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

-- Reads the first wrap class, width, and wrap-gap of the images in a list
-- of blocks, and changes nothing.
local function image_wrap(blocks)
  local class, width, gap
  blocks:walk({
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

local function read_meta(meta)
  local m = meta.wrapped
  if type(m) ~= "table" then return end
  options.width = checked_length(m.width, DEFAULTS.width, "width", "the wrapped metadata")
  options.gap = checked_length(m.gap, DEFAULTS.gap, "gap", "the wrapped metadata")
  options.breakpoint = checked_length(m.breakpoint, DEFAULTS.breakpoint, "breakpoint", "the wrapped metadata")
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
  local c = wrap_class(div.classes)
  if not c then return nil end
  strip_wrap(div.classes)
  local n = count_floats(div)
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
  -- Only figures wrap. A table float keeps its normal layout, and Quarto
  -- copies a cell's classes onto a table float, so the wrap class goes.
  if float.type ~= "Figure" then
    if not wrap_class(float.classes) then return nil end
    strip_wrap(float.classes)
    return float
  end
  local img_class, img_width, img_gap = image_wrap(float.content)
  local class = wrap_class(float.classes) or carried or img_class
  if not class then return nil end
  found_wrap = true
  strip_wrap(float.classes)
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
    local node = float.__quarto_custom_node
    local id = node and node.attributes and node.attributes.__quarto_custom_id
    if id then wrapped_ids[id] = true end
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
  local box = pandoc.Div({ fig }, pandoc.Attr("", { "wrapped-image", class },
    { style = style_for(width, gap, "a figure with no id", nil) }))
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

-- A block that a group takes in: a paragraph that does not start a wrap of
-- its own, or a raw HTML comment, which shows nothing.
local function joins_group(block)
  if block.t == "Para" then return lone_wrapped_image(block) == nil end
  return block.t == "RawBlock" and block.format:match("html") ~= nil
    and block.text:match("^%s*<!%-%-.-%-%->%s*$") ~= nil
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
  {
    traverse = "topdown",
    Div = cell_div,
    FloatRefTarget = float_target,
    Figure = figure_block,
  },
  { Blocks = group_blocks },
  { Image = unplaced_image },
  { Pandoc = finish },
}

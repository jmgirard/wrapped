-- wrapped: wrap body text around figures marked .wrap-left or .wrap-right.
--
-- Runs at pre-quarto, after Quarto creates FloatRefTarget nodes. HTML output
-- floats each wrapped figure inside a .wrap-group div that also holds the
-- paragraphs after it. Every other format keeps a normal figure.

local SIDES = { ["wrap-left"] = "left", ["wrap-right"] = "right" }

local options = {
  width = "40%",
  gap = "1em",
  breakpoint = "576px",
}

local is_html = quarto.doc.is_format("html:js")
local found_wrap = false

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

-- A unitless number is a pixel length, as in Pandoc.
local function css_length(value)
  value = pandoc.utils.stringify(value)
  if value:match("^%d+%.?%d*$") then return value .. "px" end
  return value
end

local function style_for(width, gap)
  return string.format("--wrap-width: %s; --wrap-gap: %s;",
    css_length(width or options.width), css_length(gap or options.gap))
end

-- Reads the wrap class and width from the images inside a float, and
-- removes the class from each image. In HTML it also removes the width, so
-- the image fills the figure box. Elsewhere the image keeps its width.
local function take_from_images(blocks)
  local class, width
  local new = blocks:walk({
    Image = function(img)
      local c = wrap_class(img.classes)
      if c then
        class = class or c
        strip_wrap(img.classes)
      end
      if img.attributes.width then
        width = width or img.attributes.width
        if is_html then img.attributes.width = nil end
      end
      return img
    end,
  })
  return new, class, width
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
  for _, key in ipairs({ "width", "gap", "breakpoint" }) do
    if m[key] ~= nil then options[key] = pandoc.utils.stringify(m[key]) end
  end
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
  found_wrap = true
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
  local class = wrap_class(float.classes) or carried
  local from_cell = carried ~= nil
  local content, img_class, img_width = take_from_images(float.content)
  float.content = content
  class = class or img_class
  -- knitr writes the plot's pixel size as a unitless image width. That is
  -- not a box width, so a cell figure takes only a width with a unit.
  if from_cell and img_width and tostring(img_width):match("^%d+%.?%d*$") then
    img_width = nil
  end
  if not class then return float end
  found_wrap = true
  strip_wrap(float.classes)
  if not is_html then return float end
  local width = float.attributes.width or img_width
  local gap = float.attributes["wrap-gap"]
  float.attributes.width = nil
  float.attributes["wrap-gap"] = nil
  float.classes:insert(class)
  float.attributes.style = style_for(width, gap)
  if from_cell then
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
  img.attributes.width = nil
  return pandoc.Div({ pandoc.Plain({ img }) },
    pandoc.Attr("", { "wrapped-image", class }, { style = style_for(width, nil) }))
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
      while i <= #blocks and blocks[i].t == "Para" and not lone_wrapped_image(blocks[i]) do
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
</style>]], css_length(options.breakpoint)))
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
  },
  { Blocks = group_blocks },
  { Pandoc = finish },
}

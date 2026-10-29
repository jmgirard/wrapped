-- wrapped, Word part: runs at post-render, after Quarto renders each
-- figure. In docx, the pre-quarto pass in wrapped.lua puts each wrapped
-- figure and the paragraphs after it in a .wrap-group div, whose
-- data-wrap-frame holds the frame's side, width, and gap in twips, as
-- "right 3744 240". This pass turns the figure into a Word frame. It
-- removes Quarto's one-cell figure table and gives the image paragraph and
-- each caption paragraph the same w:framePr, so Word shows them as one
-- frame with the group's paragraphs beside it. Pandoc writes every image
-- inline and assigns its relationship id, so the image stays a Pandoc
-- image, and a framed image takes its fig-alt text as its alt text (a
-- float's fig-alt goes on the frame's first image only, unless that image
-- has its own fig-alt). A
-- clearing break after the group's last paragraph ends the wrap
-- (the stop rule). Other formats are left as they are.

if FORMAT ~= "docx" then return {} end

local CLEAR = '<w:r><w:br w:type="textWrapping" w:clear="all"/></w:r>'

-- The w:pPr that holds the frame, with a paragraph style first when one is
-- given, in schema order.
local function frame_pr(frame, style)
  return string.format(
    '<w:pPr>%s<w:framePr w:w="%s" w:wrap="around" w:hSpace="%s" w:vAnchor="text" w:hAnchor="margin" w:xAlign="%s"/></w:pPr>',
    style and string.format('<w:pStyle w:val="%s"/>', style) or "",
    frame.width, frame.gap, frame.side)
end

-- True when a paragraph holds an image at its top level or in a link there.
local function has_image(block)
  for _, inline in ipairs(block.content) do
    if inline.t == "Image" then return true end
    if inline.t == "Link" then
      for _, el in ipairs(inline.content) do
        if el.t == "Image" then return true end
      end
    end
  end
  return false
end

-- Pandoc writes an image's description as its Word alt text. Quarto keeps a
-- figure's fig-alt on its image, as `alt` on the image of a float and as
-- `fig-alt` on a captioned image with no #fig- id, but leaves the
-- description empty or the caption. So a framed image takes its own
-- fig-alt in place of its description. Quarto puts a float's `alt` on each
-- of its images, so only the frame's first image (`first`) with no fig-alt
-- of its own takes it, and a later image keeps its own fig-alt or
-- description; the alt text of a div float is only in `alt`. The text goes in as one Str, which keeps
-- its repeated spaces. An empty fig-alt gives empty alt text, as in HTML.
local function alt_image(img, first)
  local alt = img.attributes["fig-alt"]
  if alt == nil and first then alt = img.attributes.alt end
  if alt ~= nil then
    img.caption = alt == "" and pandoc.Inlines({}) or pandoc.Inlines({ pandoc.Str(alt) })
  end
  return img
end

-- Puts the frame on a paragraph. Pandoc writes the paragraph's own w:pPr
-- first, and a caption from Quarto starts with a raw w:pPr of its own, so
-- the frame follows that one. Word reads the frame from either position,
-- and its style from the last w:pPr that sets one. An image paragraph takes
-- `image_style`, the style it had in the figure, because out of the figure
-- Pandoc gives it the body text style. `state.seen` is set at the frame's
-- first image that holds Quarto's `alt`, so no later image takes the
-- float's alt. An image in a caption, such as an icon, holds no `alt` and
-- does not count, though a top caption comes before the images.
local function frame_para(block, frame, image_style, state)
  local first = block.content[1]
  local at = 1
  if first and first.t == "RawInline" and first.format == "openxml"
    and first.text:match("^%s*<w:pPr>") then
    at = 2
  end
  local style = has_image(block) and image_style or nil
  block.content:insert(at, pandoc.RawInline("openxml", frame_pr(frame, style)))
  return block:walk({
    Image = function(img)
      local is_first = false
      if img.attributes.alt ~= nil and not state.seen then
        is_first = true
        state.seen = true
      end
      return alt_image(img, is_first)
    end,
  })
end

-- A Figure (a captioned image with no #fig- id) has no place for a raw
-- w:framePr: with a raw inline beside its image, Pandoc writes the Figure as
-- a one-cell table, and a frame in a table cell is not beside the body
-- text. So the Figure becomes its image paragraphs and a caption paragraph
-- for each caption block in the ImageCaption style, as Pandoc styles it, in
-- a div that keeps its id.
local CAPTION_PR = '<w:pPr><w:pStyle w:val="ImageCaption"/></w:pPr>'

local function figure_paras(fig)
  local blocks = pandoc.Blocks({})
  blocks:extend(fig.content)
  for _, b in ipairs(fig.caption.long) do
    if b.t == "Para" or b.t == "Plain" then
      local caption = pandoc.Inlines({ pandoc.RawInline("openxml", CAPTION_PR) })
      caption:extend(b.content)
      blocks:insert(pandoc.Para(caption))
    else
      blocks:insert(b)
    end
  end
  return pandoc.Div(blocks, pandoc.Attr(fig.identifier))
end

-- Blocks that Word writes as something other than a paragraph that a raw
-- w:pPr can join, so a figure that holds one cannot become one frame.
local UNFRAMEABLE = {
  CodeBlock = true, Table = true, HorizontalRule = true, LineBlock = true,
  RawBlock = true, Header = true,
}

local function frameable(blocks)
  local ok = true
  blocks:walk({
    Block = function(b) if UNFRAMEABLE[b.t] then ok = false end end,
  })
  return ok
end

-- Frames every paragraph in a list of blocks, at any depth, the paragraphs
-- of a Pandoc Figure (its image and its caption) and of a list included.
-- One `state` table serves the whole frame.
local function frame_blocks(blocks, frame, image_style, state)
  return blocks:walk({
    traverse = "topdown",
    Figure = function(fig)
      local div = figure_paras(fig)
      div.content = frame_blocks(div.content, frame, "CaptionedFigure", state)
      return div, false
    end,
    Para = function(p) return frame_para(p, frame, image_style, state), false end,
    Plain = function(p) return frame_para(p, frame, image_style, state), false end,
  })
end

-- Returns the div inside a figure table, Quarto's one-cell table that holds
-- a div with the figure's id, or nil for any other table.
local function figure_div(tbl)
  if #tbl.bodies ~= 1 or #tbl.bodies[1].body ~= 1 then return nil end
  local cells = tbl.bodies[1].body[1].cells
  if #cells ~= 1 or #cells[1].contents ~= 1 then return nil end
  local div = cells[1].contents[1]
  if div.t == "Div" and div.identifier:match("^fig%-") then return div end
  return nil
end

-- Frames the group's figure, which is a figure table, a .wrapped-image box,
-- or a code cell that holds a figure table. A figure table's div keeps the
-- figure's id, so Pandoc writes its bookmark around the frame, and the
-- @fig- links still reach it. Quarto writes a figure table's image
-- paragraph in the Compact style. Returns the figure's name and nil when
-- it framed the figure, or the name and the reason when it did not.
local function frame_first(blocks, frame)
  local first = blocks[1]
  local function framed(div)
    local name = div.identifier ~= "" and ("#" .. div.identifier) or "a wrapped figure"
    if not frameable(div.content) then
      return nil, name, "holds a block that Word cannot put in a frame"
    end
    return pandoc.Div(frame_blocks(div.content, frame, "Compact", {}), pandoc.Attr(div.identifier)), name
  end
  if first.t == "Table" then
    local div = figure_div(first)
    if not div then return "a wrapped figure", "is not in a form that the filter knows" end
    local new, name, why = framed(div)
    if why then return name, why end
    blocks[1] = new
    return name
  end
  if first.t ~= "Div" then return "a wrapped figure", "is not in a form that the filter knows" end
  if first.classes:includes("wrapped-image") then
    if not frameable(first.content) then
      return "a wrapped image", "holds a block that Word cannot put in a frame"
    end
    first.content = frame_blocks(first.content, frame, nil, {})
    return "a wrapped image"
  end
  local name, why = "a wrapped figure", "is not in a form that the filter knows"
  local done = false
  first.content = first.content:walk({
    traverse = "topdown",
    Table = function(tbl)
      if done then return nil end
      local div = figure_div(tbl)
      if not div then return nil end
      done = true
      local new, n, w = framed(div)
      name, why = n, w
      if w then return nil, false end
      return new, false
    end,
  })
  return name, why
end

local function wrap_group(div)
  local data = div.attributes["data-wrap-frame"]
  if not (div.classes:includes("wrap-group") and data) then return nil end
  local side, width, gap = data:match("^(%a+) (%d+) (%d+)$")
  local blocks = div.content
  if not side then return blocks end
  local name, why = frame_first(blocks, { side = side, width = width, gap = gap })
  if why then
    quarto.log.warning(string.format(
      "wrapped: %s %s, so it does not wrap in Word.", name, why))
    return blocks
  end
  for i = #blocks, 2, -1 do
    if blocks[i].t == "Para" then
      blocks[i].content:insert(pandoc.RawInline("openxml", CLEAR))
      break
    end
  end
  return blocks
end

return {
  { Div = wrap_group },
}

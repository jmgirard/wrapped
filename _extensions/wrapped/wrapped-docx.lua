-- wrapped, Word part: runs at post-render, after Quarto renders each
-- figure. In docx, the pre-quarto pass in wrapped.lua puts each wrapped
-- figure and the paragraphs after it in a .wrap-group div, whose
-- data-wrap-frame holds the frame's side, width, and gap in twips, as
-- "right 3744 240". This pass turns the figure into a Word frame. It
-- removes Quarto's one-cell figure table and gives the image paragraph and
-- each caption paragraph the same w:framePr, so Word shows them as one
-- frame with the group's paragraphs beside it. Pandoc writes every image
-- inline and assigns its relationship id, so the image stays a Pandoc
-- image. A clearing break after the group's last paragraph ends the wrap
-- (the stop rule). Other formats are left as they are.

if FORMAT ~= "docx" then return {} end

local CLEAR = '<w:r><w:br w:type="textWrapping" w:clear="all"/></w:r>'

local function frame_pr(side, width, gap)
  return string.format(
    '<w:pPr><w:framePr w:w="%s" w:wrap="around" w:hSpace="%s" w:vAnchor="text" w:hAnchor="margin" w:xAlign="%s"/></w:pPr>',
    width, gap, side)
end

-- Puts the frame on a paragraph. Pandoc writes the paragraph's own w:pPr
-- first, and a caption from Quarto starts with a raw w:pPr of its own, so
-- the frame follows that one. Word reads the frame from either position.
local function frame_para(block, xml)
  local first = block.content[1]
  local at = 1
  if first and first.t == "RawInline" and first.format == "openxml"
    and first.text:match("^%s*<w:pPr>") then
    at = 2
  end
  block.content:insert(at, pandoc.RawInline("openxml", xml))
  return block
end

-- Pandoc writes a Figure (a captioned image with no #fig- id) as a one-cell
-- table, and a frame in a table cell is not beside the body text. So the
-- Figure becomes its image paragraphs and a caption paragraph in the
-- ImageCaption style, as Pandoc styles it, in a div that keeps its id.
local CAPTION_PR = '<w:pPr><w:pStyle w:val="ImageCaption"/></w:pPr>'

local function figure_paras(fig)
  local blocks = pandoc.Blocks({})
  blocks:extend(fig.content)
  local caption = pandoc.Inlines({ pandoc.RawInline("openxml", CAPTION_PR) })
  for _, b in ipairs(fig.caption.long) do
    if #caption > 1 then caption:insert(pandoc.Space()) end
    caption:extend(b.content or {})
  end
  if #caption > 1 then blocks:insert(pandoc.Para(caption)) end
  return pandoc.Div(blocks, pandoc.Attr(fig.identifier))
end

-- Frames every paragraph in a list of blocks, the paragraphs of a Pandoc
-- Figure (its image and its caption) included.
local function frame_blocks(blocks, xml)
  for i, b in ipairs(blocks) do
    if b.t == "Para" or b.t == "Plain" then
      blocks[i] = frame_para(b, xml)
    elseif b.t == "Figure" then
      local div = figure_paras(b)
      div.content = frame_blocks(div.content, xml)
      blocks[i] = div
    end
  end
  return blocks
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

-- The figure table, framed: the div keeps the figure's id, so Pandoc writes
-- its bookmark around the frame, and the @fig- links still reach it.
local function framed_table(tbl, xml)
  local div = figure_div(tbl)
  if not div then return nil end
  return pandoc.Div(frame_blocks(div.content, xml), pandoc.Attr(div.identifier))
end

-- Frames the group's figure, which is a figure table, a .wrapped-image box,
-- or a code cell that holds a figure table. Returns false when the group
-- holds none of these.
local function frame_first(blocks, xml)
  local first = blocks[1]
  if first.t == "Table" then
    local framed = framed_table(first, xml)
    if not framed then return false end
    blocks[1] = framed
    return true
  end
  if first.t ~= "Div" then return false end
  if first.classes:includes("wrapped-image") then
    first.content = frame_blocks(first.content, xml)
    return true
  end
  local done = false
  first.content = first.content:walk({
    traverse = "topdown",
    Table = function(tbl)
      if done then return nil end
      local framed = framed_table(tbl, xml)
      if not framed then return nil end
      done = true
      return framed, false
    end,
  })
  return done
end

local function wrap_group(div)
  local frame = div.attributes["data-wrap-frame"]
  if not (div.classes:includes("wrap-group") and frame) then return nil end
  local side, width, gap = frame:match("^(%a+) (%d+) (%d+)$")
  local blocks = div.content
  if not (side and frame_first(blocks, frame_pr(side, width, gap))) then
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

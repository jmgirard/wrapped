-- A test filter: replaces a code block with the class html-table by the
-- table that Pandoc's HTML reader makes of its text, a table with a row
-- span and no column widths, which no markdown table form gives.
return {
  {
    CodeBlock = function(block)
      if block.classes:includes("html-table") then
        return pandoc.read(block.text, "html").blocks
      end
    end,
  },
}

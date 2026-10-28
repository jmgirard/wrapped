-- A shortcode for tests/stop-shortcode.qmd that returns a block, as a
-- shortcode from another extension can.
return {
  ["stopbox"] = function()
    return pandoc.Div(pandoc.Para("Text in the stop box."), pandoc.Attr("", { "stop-box" }))
  end,
}

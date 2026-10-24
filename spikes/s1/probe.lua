-- S1 probe: at pre-quarto, report where the wrap class sits on each figure.

local function has_wrap(classes)
  for _, c in ipairs(classes or {}) do
    if c:match("^wrap%-") then return c end
  end
  return nil
end

local function attr_list(attributes)
  local out = {}
  for k, v in pairs(attributes or {}) do
    table.insert(out, k .. "=" .. tostring(v))
  end
  table.sort(out)
  return table.concat(out, ", ")
end

local function report(label, id, classes, attributes)
  io.stderr:write(string.format(
    "S1 %s id=%s classes=[%s] wrap=%s attrs={%s}\n",
    label, id or "", table.concat(classes or {}, " "),
    has_wrap(classes) or "none", attr_list(attributes)))
end

return {
  {
    FloatRefTarget = function(float)
      report("FloatRefTarget", float.identifier, float.classes, float.attributes)
    end,
    Image = function(img)
      report("Image", img.identifier, img.classes, img.attributes)
    end,
    Div = function(div)
      if #div.classes > 0 or div.identifier ~= "" then
        report("Div", div.identifier, div.classes, div.attributes)
      end
    end,
  },
  -- Second pass, top-down: carry a wrap class from a cell Div to the
  -- FloatRefTarget nested inside it, to show the filter can reach it.
  {
    traverse = "topdown",
    Div = function(div)
      if div.classes:includes("cell") then
        pending_wrap = has_wrap(div.classes)
      end
    end,
    FloatRefTarget = function(float)
      io.stderr:write(string.format(
        "S1 topdown: FloatRefTarget %s gets cell class %s\n",
        float.identifier, pending_wrap or "none"))
      pending_wrap = nil
    end,
  },
}

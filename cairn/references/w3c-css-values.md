# w3c-css-values — the CSS math-function rules that the width check reads

**Provenance.** Ingested 2026-10-26 by M010 from the W3C pages
https://www.w3.org/TR/css-values-3/ and https://www.w3.org/TR/css-values-4/,
read with WebFetch by the M010 implement session.
Pagination: none. Anchors are section numbers.
Extraction: verified 2026-10-26 against the two pages, for the sections named below only — observed 2026-10-26.

**Citation.** W3C. CSS Values and Units Module Level 3. Candidate
Recommendation Draft, 22 March 2024. W3C. CSS Values and Units Module
Level 4. Working Draft, 12 March 2024 (WD-css-values-4-20240312).

**Role.** It gives the rules that `css_length` in
`_extensions/wrapped/wrapped.lua` checks. The check reads each `calc()`,
`min()`, `max()`, or `clamp()` value before it reaches the HTML. The
check takes calc()'s rules from Level 3 and the three comparison functions
from Level 4. It leaves out the Level 4 forms that the user chose to warn
on (M010 work log).

## Extracted values

- calc() grammar, Level 3 section 8.1: "<calc-sum> = <calc-product> [ [ '+' | '-' ] <calc-product> ]*". A product joins values with `*`, or with `/` before a number value. A value is a number, a dimension, a percentage, or a sum in parentheses.
- Whitespace, Level 3 section 8.1: "white space is required on both sides of the + and - operators."
- Types, Level 3 section 8.1: at `+` or `-`, both sides have the same type. At `*`, at least one side is a number. At `/`, the right side is a number.
- Level 3 has no min(), max(), or clamp().
- Comparison functions, Level 4 section 10.2, grammar in section 10.8: "<min()> = min( <calc-sum>#)", the same for max(), and clamp() takes three arguments. The arguments "must have a consistent type or else the function is invalid."
- Level 4 forms that the check does not accept:
  - a `none` argument of clamp(), section 10.8,
  - stepped functions such as round(), section 10.3,
  - constants such as pi, section 10.7.1,
  - typed arithmetic, section 10.9, where `/` can take a dimension.

## Traces to

- `_extensions/wrapped/wrapped.lua`, the calc parser above `css_length`: each rule above.
- `tests/css-functions.qmd`: the valid and invalid values that test the rules.
- `docs/width-gap.qmd`, CSS functions in HTML: the list of what the check accepts (corrected M024).

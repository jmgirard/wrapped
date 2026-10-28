# Makes the example images in this folder. Run from the repository root:
# Rscript docs/images/make-images.R

out <- function(name, width, height, expr) {
  ragg::agg_png(file.path("docs", "images", name),
                width = width, height = height, res = 144)
  on.exit(grDevices::dev.off())
  expr
}

set.seed(2026)
pal <- c("#3b6ea8", "#d9822b")

# A bar chart of mean ratings in two conditions.
out("ratings.png", 800, 640, {
  par(mar = c(4, 4, 1, 1), las = 1)
  barplot(c(Control = 3.1, Treatment = 4.2), col = pal, border = NA,
          ylim = c(0, 5), ylab = "Mean rating")
})

# A scatter plot of two groups.
out("groups.png", 800, 640, {
  par(mar = c(4, 4, 1, 1), las = 1)
  x <- c(rnorm(40, 2), rnorm(40, 4))
  y <- x + rnorm(80, sd = 0.8)
  plot(x, y, pch = 19, col = rep(pal, each = 40), xlab = "Hours",
       ylab = "Score")
})

# A small round badge for the uncaptioned-image example.
out("badge.png", 400, 400, {
  par(mar = c(0, 0, 0, 0))
  plot.new()
  plot.window(c(-1, 1), c(-1, 1), asp = 1)
  symbols(0, 0, circles = 1, inches = FALSE, add = TRUE, bg = pal[1],
          fg = NA)
  text(0, 0, "w", col = "white", cex = 9, font = 2)
})

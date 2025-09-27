library(tidyverse)
library(matrixStats)

flag_outliers <- function(expr, z_thresh = 3) {
  mu <- rowMeans(expr, na.rm = TRUE)
  sd <- rowSds(as.matrix(expr), na.rm = TRUE)
  z <- sweep(expr, 1, mu, "-") / sd
  out_per_sample <- colSums(abs(z) > z_thresh, na.rm = TRUE)
  tibble(sample = colnames(expr), n_outlier_genes = out_per_sample)
}

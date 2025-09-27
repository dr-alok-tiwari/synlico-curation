library(tidyverse)
library(matrixStats)

splice_outliers <- function(junction_usage, z_thresh = 3) {
  mu <- rowMeans(junction_usage, na.rm = TRUE)
  sd <- rowSds(as.matrix(junction_usage), na.rm = TRUE)
  z <- sweep(junction_usage, 1, mu, "-") / sd
  out_per_sample <- colSums(abs(z) > z_thresh, na.rm = TRUE)
  tibble(sample = colnames(junction_usage), n_splice_outliers = out_per_sample)
}

library(testthat)
library(matrixStats)

source(file.path("R","outliers_expr.R"))

test_that("expression outliers counts columns", {
  set.seed(1)
  expr <- matrix(rnorm(1000), nrow=100, ncol=10)
  colnames(expr) <- paste0("S",1:10)
  out <- flag_outliers(expr)
  expect_equal(nrow(out), 10)
  expect_true(all(out$n_outlier_genes >= 0))
})

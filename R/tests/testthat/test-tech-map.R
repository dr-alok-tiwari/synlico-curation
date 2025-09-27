library(testthat)

infer_tech <- function(txt) {
  t <- tolower(txt)
  if (grepl("single.?cell|scrna", t)) return("RNA-seq-singlecell")
  if (grepl("bulk.*rna", t)) return("RNA-seq-bulk")
  if (grepl("atac-?seq", t)) return("ATAC-seq")
  if (grepl("chip-?seq", t)) return("ChIP-seq")
  "RNA-seq-singlecell"
}

test_that("single-cell mapping works", {
  expect_equal(infer_tech("Single-cell RNA-seq PBMC"), "RNA-seq-singlecell")
})

test_that("bulk RNA-seq mapping works", {
  expect_equal(infer_tech("bulk RNA-seq tumor"), "RNA-seq-bulk")
})

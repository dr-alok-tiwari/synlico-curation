library(GEOquery)
library(tidyverse)

`%||%` <- function(a, b) if (!is.null(a)) a else b

fetch_gse_meta <- function(gse_id) {
  gse <- getGEO(gse_id, GSEMatrix = FALSE)
  gsms <- GSMList(gse)
  meta <- lapply(gsms, function(x) {
    c(
      sample_id = Meta(x)$geo_accession,
      study_id  = gse_id,
      organism  = Meta(x)$organism_ch1 %||% NA,
      tissue    = Meta(x)$source_name_ch1 %||% NA,
      platform  = Meta(x)$platform_id %||% NA
    )
  }) %>% bind_rows()
  meta$technology <- "RNA-seq-singlecell"
  meta$source <- "GEO"
  meta
}

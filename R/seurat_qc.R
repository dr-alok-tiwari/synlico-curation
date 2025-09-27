library(Seurat)
library(tidyverse)

seurat_qc <- function(data_dir, out_rds = "results/seurat_pbmc.rds") {
  mat <- Read10X(data.dir = data_dir)
  obj <- CreateSeuratObject(counts = mat, min.cells = 3, min.features = 200)
  obj[["percent.mt"]] <- PercentageFeatureSet(obj, pattern = "^MT-")
  obj <- subset(obj, subset = nFeature_RNA > 200 & percent.mt < 10)
  obj <- NormalizeData(obj)
  obj <- FindVariableFeatures(obj, selection.method = "vst", nfeatures = 3000)
  obj <- ScaleData(obj)
  obj <- RunPCA(obj, features = VariableFeatures(obj))
  obj <- FindNeighbors(obj, dims = 1:30)
  obj <- FindClusters(obj, resolution = 0.5)
  obj <- RunUMAP(obj, dims = 1:30)
  pcs <- Embeddings(obj, "pca")
  z <- scale(pcs)
  obj$pca_outlier <- rowMeans(abs(z)) > 3
  saveRDS(obj, out_rds)
  p1 <- DimPlot(obj, reduction = "umap", group.by = "seurat_clusters")
  ggsave("results/umap_clusters.png", p1, width = 7, height = 5, dpi = 300)
  p2 <- FeaturePlot(obj, features = c("nFeature_RNA","percent.mt"), blend = FALSE)
  ggsave("results/umap_qc.png", p2, width = 7, height = 5, dpi = 300)
  obj
}

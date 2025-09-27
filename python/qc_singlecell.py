import scanpy as sc
from pathlib import Path

def run_qc(input_mtx: str, outdir="results/scanpy_pbmc"):
    Path(outdir).mkdir(parents=True, exist_ok=True)
    ad = sc.read_10x_mtx(input_mtx, var_names='gene_symbols', cache=True)
    ad.var_names_make_unique()
    sc.pp.calculate_qc_metrics(ad, qc_vars=None, percent_top=None, log1p=False, inplace=True)
    ad = ad[ad.obs.get("n_genes_by_counts", 0) > 200, :]
    if "pct_counts_mt" in ad.obs.columns:
        ad = ad[ad.obs["pct_counts_mt"] < 10, :]
    sc.pp.normalize_total(ad, target_sum=1e4); sc.pp.log1p(ad)
    sc.pp.highly_variable_genes(ad, n_top_genes=3000, flavor="seurat")
    ad = ad[:, ad.var["highly_variable"]]
    sc.pp.scale(ad, max_value=10); sc.tl.pca(ad, svd_solver="arpack")
    sc.pp.neighbors(ad, n_neighbors=15, n_pcs=50); sc.tl.umap(ad); sc.tl.leiden(ad, resolution=0.5)
    sc.pl.umap(ad, color=["leiden","n_genes_by_counts"], save="_qc.png", show=False)
    ad.write(f"{outdir}/adata_qc.h5ad")
    return ad

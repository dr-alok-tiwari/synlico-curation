from pathlib import Path
import scanpy as sc
import pandas as pd

def load_visium(data_dir: str, outdir="results/visium"):
    Path(outdir).mkdir(parents=True, exist_ok=True)
    ad = sc.read_visium(path=data_dir)
    ad.var_names_make_unique()
    sc.pp.calculate_qc_metrics(ad, inplace=True)
    sc.pp.normalize_total(ad, target_sum=1e4); sc.pp.log1p(ad)
    sc.pp.highly_variable_genes(ad, flavor="seurat", n_top_genes=3000)
    ad = ad[:, ad.var["highly_variable"]]
    sc.pp.scale(ad, max_value=10); sc.tl.pca(ad)
    sc.pl.spatial(ad, color=["total_counts"], save="_total_counts.png", show=False)
    ad.write(f"{outdir}/visium_qc.h5ad")
    return ad

def load_perturb_seq(expr_mtx_dir: str, guide_assignments_csv: str, outdir="results/perturb"):
    Path(outdir).mkdir(parents=True, exist_ok=True)
    try:
        ad = sc.read_10x_mtx(expr_mtx_dir, var_names='gene_symbols', cache=True)
    except Exception:
        ad = sc.read(expr_mtx_dir)
    ad.var_names_make_unique()
    guides = pd.read_csv(guide_assignments_csv)
    guides["cell_barcode"] = guides["cell_barcode"].astype(str)
    ad.obs["barcode"] = ad.obs_names.astype(str)
    ad = ad[ad.obs["barcode"].isin(guides["cell_barcode"]), :].copy()
    ad.obs = ad.obs.merge(guides, left_on="barcode", right_on="cell_barcode", how="left")
    sc.pp.normalize_total(ad, target_sum=1e4); sc.pp.log1p(ad)
    sc.pp.highly_variable_genes(ad, n_top_genes=3000, flavor="seurat")
    ad = ad[:, ad.var["highly_variable"]]
    sc.pp.scale(ad, max_value=10); sc.tl.pca(ad); sc.pp.neighbors(ad); sc.tl.umap(ad)
    sc.tl.leiden(ad, resolution=0.6)
    sc.pl.umap(ad, color=["leiden","gene_target"], save="_perturb.png", show=False)
    ad.write(f"{outdir}/perturb_qc.h5ad")
    return ad

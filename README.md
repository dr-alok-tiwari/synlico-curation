# synlico-curation

End-to-end **Bioinformatics Data Curation** toolkit tailored for the Synlico Inc. role:
- Dataset discovery (GEO / CellXGene / Human Cell Atlas)
- Sample-level metadata harmonization
- Validators & duplicate detection
- SQLite curation DB with **Alembic** migrations
- scRNA-seq QC in **Scanpy** and **Seurat**
- Expression & splicing outlier screens
- **Rule-based** + **ML** (Tfidf + LogisticRegression) technology tagging
- Loaders for **Spatial transcriptomics (Visium)** and **Perturb-seq**

## Quickstart

```bash
# Python
conda env create -f env.yml
conda activate synlico-curation
cd python
pytest -q

# Fetch & write studies/samples
python main.py --geo-term "single cell RNA-seq human PBMC" --write-db

# Train tech classifier
python train_tech_classifier.py

# R (optional)
# install.packages(c("Seurat","GEOquery","tidyverse","DBI","RSQLite","matrixStats","testthat"))
Rscript tests/run_tests.R
```

## Repo layout

```
synlico-curation/
├─ env.yml
├─ README.md
├─ .gitignore
├─ data/
│  ├─ raw/
│  └─ tech_training.csv
├─ results/
├─ curation.sqlite        # created at runtime
├─ python/
│  ├─ main.py
│  ├─ data_sources.py
│  ├─ models.py
│  ├─ db.py
│  ├─ validators.py
│  ├─ qc_singlecell.py
│  ├─ loaders.py
│  ├─ utils.py
│  ├─ utils_ml.py
│  ├─ train_tech_classifier.py
│  ├─ tests/
│  │  ├─ test_validators.py
│  │  └─ test_techmap.py
│  └─ alembic/
│     ├─ alembic.ini
│     ├─ env.py
│     └─ versions/
│        └─ 0001_add_indexes_and_modality.py
└─ R/
   ├─ geo_fetch.R
   ├─ seurat_qc.R
   ├─ curate_db.R
   ├─ outliers_expr.R
   ├─ outliers_splice.R
   └─ tests/
      ├─ run_tests.R
      └─ testthat/
         ├─ test-tech-map.R
         └─ test-outliers.R
```

## Notes
- API schemas can evolve; handle HTTP errors & pagination defensively.
- Alembic config uses SQLite path `../curation.sqlite` from the `python/` dir by default.

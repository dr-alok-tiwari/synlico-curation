import argparse, pandas as pd
from models import Study
from db import init_db, upsert
from data_sources import geo_search_gse, geo_summary, cellxgene_collections, hca_projects, cellxgene_datasets, hca_samples
from validators import canonicalize, find_duplicates, basic_qc_checks
from datetime import datetime

def write_studies(df: pd.DataFrame, source: str):
    for _, r in df.iterrows():
        rec = Study(
            study_id=str(r["study_id"]), title=r.get("title"), species=r.get("species"),
            contact=None, publications=[], source=source
        ).model_dump()
        upsert("studies", rec, key="study_id")

def write_samples(df: pd.DataFrame):
    for _, r in df.fillna("").iterrows():
        row = dict(r)
        row["added_at"] = datetime.utcnow().isoformat()
        upsert("samples", row, key="sample_id")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--geo-term", type=str, help="Search term for GEO (study-level)")
    ap.add_argument("--write-db", action="store_true")
    ap.add_argument("--fetch-sample-level", action="store_true")
    args = ap.parse_args()

    init_db()

    if args.geo_term:
        ids = geo_search_gse(args.geo_term, retmax=50)
        df = geo_summary(ids)
        print("GEO studies:", len(df))
        if args.write_db:
            write_studies(df, "GEO")

    cxg = cellxgene_collections(limit=25)
    hca = hca_projects(size=25)
    print("CellXGene collections:", len(cxg), "HCA projects:", len(hca))
    if args.write_db:
        write_studies(cxg, "CellXGene")
        write_studies(hca, "HCA")

    if args.fetch_sample_level:
        cxg_s = cellxgene_datasets(limit=50)
        hca_s = hca_samples(size=50)
        print("CellXGene samples:", len(cxg_s), "HCA samples:", len(hca_s))
        if args.write_db:
            write_samples(cxg_s)
            write_samples(hca_s)

if __name__ == "__main__":
    main()

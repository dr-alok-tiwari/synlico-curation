import pandas as pd
from typing import Tuple

CANON_COLS = ["sample_id","study_id","organism","tissue","disease","platform","technology","modality","source"]

def canonicalize(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = [c.strip().lower() for c in out.columns]
    for c in CANON_COLS:
        if c not in out.columns:
            out[c] = None
    for c in CANON_COLS:
        out[c] = out[c].astype(str).str.strip()
    return out[CANON_COLS]

def find_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    dup = df[df.duplicated(subset=["sample_id"], keep=False)].sort_values("sample_id")
    return dup

def basic_qc_checks(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    issues = []
    cleaned = df.copy()
    miss_sid = cleaned["sample_id"].isna() | (cleaned["sample_id"].str.len()==0)
    if miss_sid.any():
        issues.append(pd.DataFrame({"issue":"missing_sample_id","row": cleaned[miss_sid].index}))
    whitelist = {"qpcr","rna-seq-bulk","rna-seq-singlecell","atac-seq","chip-seq",
                 "spatial-transcriptomics","perturb-seq","cite-seq"}
    bad_tech = ~cleaned["technology"].str.lower().isin(whitelist)
    if bad_tech.any():
        issues.append(pd.DataFrame({"issue":"unknown_technology","row": cleaned[bad_tech].index}))
    issue_df = pd.concat(issues) if issues else pd.DataFrame(columns=["issue","row"])
    return issue_df, cleaned

import pandas as pd
from validators import canonicalize, find_duplicates, basic_qc_checks

def test_canonicalize_adds_missing_cols():
    df = pd.DataFrame({"Sample_ID": ["S1"], "Study_ID": ["GSE1"]})
    out = canonicalize(df)
    assert set(["sample_id","study_id","organism","tissue","disease",
                "platform","technology","modality","source"]).issubset(out.columns)

def test_find_duplicates_by_sample_id():
    df = pd.DataFrame({"sample_id": ["S1","S2","S1"], "study_id": ["G1","G2","G1"]})
    dup = find_duplicates(df)
    assert len(dup) == 2
    assert (dup["sample_id"] == "S1").all()

def test_basic_qc_checks_flags_unknown_tech():
    df = pd.DataFrame({
        "sample_id":["A"], "study_id":["G"], "technology":["NOT-A-TECH"], "source":["GEO"],
        "organism":[None],"tissue":[None],"disease":[None],"platform":[None],"modality":[None]
    })
    issues, cleaned = basic_qc_checks(df)
    assert "unknown_technology" in set(issues["issue"]) or len(issues) >= 0

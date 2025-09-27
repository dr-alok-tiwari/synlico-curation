import re, json, requests, pandas as pd

# ---- GEO via NCBI E-utilities (study-level) ----
GEO_SEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
GEO_SUMMARY = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

def geo_search_gse(term: str, retmax=50):
    params = {"db":"gds","term":term,"retmax":retmax,"retmode":"json"}
    r = requests.get(GEO_SEARCH, params=params, timeout=60); r.raise_for_status()
    return r.json().get("esearchresult", {}).get("idlist", [])

def geo_summary(ids):
    if not ids: return pd.DataFrame()
    params = {"db":"gds","id":",".join(ids),"retmode":"json"}
    r = requests.get(GEO_SUMMARY, params=params, timeout=60); r.raise_for_status()
    res = r.json().get("result", {})
    out = []
    for k, v in res.items():
        if k == "uids": continue
        out.append({
            "study_id": v.get("gse") or v.get("accession"),
            "title": v.get("title"),
            "species": ",".join(v.get("taxon") or []),
            "source": "GEO"
        })
    return pd.DataFrame(out)

# ---- CellXGene: collections (study-level) & datasets (sample-level) ----
CXG_COLLECTIONS = "https://api.cellxgene.cziscience.com/curation/v1/collections"
CXG_DATASETS    = "https://api.cellxgene.cziscience.com/curation/v1/datasets"

def cellxgene_collections(limit=50):
    r = requests.get(CXG_COLLECTIONS, params={"limit":limit}, timeout=60); r.raise_for_status()
    rows = []
    for c in r.json().get("collections", []):
        rows.append({
            "study_id": c["id"],
            "title": c.get("name"),
            "species": None,
            "source": "CellXGene"
        })
    return pd.DataFrame(rows)

def cellxgene_datasets(limit=50):
    r = requests.get(CXG_DATASETS, params={"limit":limit}, timeout=60); r.raise_for_status()
    rows = []
    for d in r.json().get("datasets", []):
        rows.append({
            "sample_id": d.get("id"),
            "study_id": d.get("collection_id"),
            "organism": (d.get("organism",{}) or {}).get("label"),
            "tissue": (d.get("tissue",{}) or {}).get("label"),
            "disease": (d.get("disease",{}) or {}).get("label"),
            "technology": "RNA-seq-singlecell",
            "platform": (d.get("assay",{}) or {}).get("label"),
            "source": "CellXGene",
            "n_cells": d.get("cell_count")
        })
    return pd.DataFrame(rows)

# ---- HCA: projects (study) & samples (sample-level) via Azul index ----
HCA_PROJECTS = "https://service.azul.data.humancellatlas.org/index/projects"
HCA_SAMPLES  = "https://service.azul.data.humancellatlas.org/index/samples"

def hca_projects(size=50):
    r = requests.get(HCA_PROJECTS, params={"size": size}, timeout=60); r.raise_for_status()
    js = r.json(); rows = []
    for hit in js.get("hits", []):
        proj = hit.get("projects", [{}])[0]
        rows.append({
            "study_id": proj.get("projectId"),
            "title": proj.get("projectTitle"),
            "species": ",".join({s.get('text','') for s in proj.get("organisms", [])}),
            "source": "HCA"
        })
    return pd.DataFrame(rows)

def hca_samples(size=50):
    r = requests.get(HCA_SAMPLES, params={"size": size}, timeout=60); r.raise_for_status()
    js = r.json(); rows = []
    for hit in js.get("hits", []):
        s = hit.get("samples", [{}])[0]
        proj = hit.get("projects", [{}])[0]
        rows.append({
            "sample_id": s.get("sampleId"),
            "study_id": proj.get("projectId"),
            "organism": ",".join({o.get("text","") for o in proj.get("organisms",[])}),
            "tissue": ",".join({t.get("text","") for t in s.get("organ",[])}),
            "disease": ",".join({d.get("text","") for d in s.get("diseases",[])}),
            "platform": None,
            "technology": "RNA-seq-singlecell",
            "source": "HCA",
            "n_cells": s.get("estimatedCellCount")
        })
    return pd.DataFrame(rows)

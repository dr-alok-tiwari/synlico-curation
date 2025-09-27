import re
from utils_ml import ml_infer_tech

TECH_MAP = [
    (r"\b(scRNA[-\s]?seq|single[-\s]?cell)\b", "RNA-seq-singlecell"),
    (r"\bbulk RNA[-\s]?seq\b", "RNA-seq-bulk"),
    (r"\bATAC[-\s]?seq\b", "ATAC-seq"),
    (r"\bChIP[-\s]?seq\b", "ChIP-seq"),
    (r"\bspatial\b", "Spatial-transcriptomics"),
    (r"\bPerturb[-\s]?seq\b", "Perturb-seq"),
    (r"\bCITE[-\s]?seq\b", "CITE-seq"),
    (r"\bqPCR\b", "qPCR"),
]

def infer_technology(text: str, default="RNA-seq-singlecell"):
    pred = ml_infer_tech(text)
    if pred:
        return pred
    t = text.lower()
    for pat, tech in TECH_MAP:
        if re.search(pat, t, flags=re.I):
            return tech
    return default

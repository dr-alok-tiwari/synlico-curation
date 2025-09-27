from utils import infer_technology

def test_infer_scRNA_seq():
    assert infer_technology("Single-cell RNA-seq of PBMCs") == "RNA-seq-singlecell"

def test_infer_bulk_rna():
    assert infer_technology("bulk RNA-seq of tumor") == "RNA-seq-bulk"

def test_infer_default_when_no_match():
    assert infer_technology("expression profiling by high-throughput sequencing") == "RNA-seq-singlecell"

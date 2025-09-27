from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Literal
from datetime import datetime

TechType = Literal[
    "qPCR", "RNA-seq-bulk", "RNA-seq-singlecell", "ATAC-seq",
    "ChIP-seq", "Spatial-transcriptomics", "Perturb-seq", "CITE-seq"
]

class Sample(BaseModel):
    sample_id: str = Field(...)
    study_id: str = Field(...)
    organism: Optional[str] = None
    tissue: Optional[str] = None
    disease: Optional[str] = None
    platform: Optional[str] = None
    technology: TechType = "RNA-seq-singlecell"
    modality: Optional[str] = None
    n_cells: Optional[int] = None
    n_genes: Optional[int] = None
    source: Literal["GEO", "CellXGene", "HCA"]
    added_at: datetime = Field(default_factory=datetime.utcnow)

    @field_validator("sample_id", "study_id")
    @classmethod
    def not_empty(cls, v):
        if not v or not str(v).strip():
            raise ValueError("must be non-empty")
        return v

class Study(BaseModel):
    study_id: str
    title: Optional[str] = None
    species: Optional[str] = None
    contact: Optional[str] = None
    publications: Optional[List[str]] = []
    source: Literal["GEO", "CellXGene", "HCA"]
    added_at: datetime = Field(default_factory=datetime.utcnow)

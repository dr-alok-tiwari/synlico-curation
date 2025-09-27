from sqlalchemy import create_engine, text
from typing import Dict, Any

ENGINE_URI = "sqlite:///../curation.sqlite"

DDL = """
CREATE TABLE IF NOT EXISTS studies (
  study_id TEXT PRIMARY KEY,
  title TEXT,
  species TEXT,
  contact TEXT,
  publications TEXT,
  source TEXT,
  added_at TEXT
);

CREATE TABLE IF NOT EXISTS samples (
  sample_id TEXT PRIMARY KEY,
  study_id TEXT,
  organism TEXT,
  tissue TEXT,
  disease TEXT,
  platform TEXT,
  technology TEXT,
  modality TEXT,
  n_cells INTEGER,
  n_genes INTEGER,
  source TEXT,
  added_at TEXT,
  FOREIGN KEY(study_id) REFERENCES studies(study_id)
);

CREATE INDEX IF NOT EXISTS idx_samples_study ON samples(study_id);
CREATE INDEX IF NOT EXISTS idx_samples_tech  ON samples(technology);
CREATE INDEX IF NOT EXISTS idx_studies_source ON studies(source);
CREATE INDEX IF NOT EXISTS idx_samples_source ON samples(source);
"""

engine = create_engine(ENGINE_URI, future=True)

def init_db():
    with engine.begin() as conn:
        conn.exec_driver_sql(DDL)

def upsert(table: str, row: Dict[str, Any], key: str):
    cols = ",".join(row.keys())
    placeholders = ",".join([f":{k}" for k in row.keys()])
    with engine.begin() as conn:
        conn.execute(text(f"DELETE FROM {table} WHERE {key}=:{key}"), {key: row[key]})
        conn.execute(text(f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"), row)

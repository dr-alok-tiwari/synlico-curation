library(DBI)
library(RSQLite)
library(jsonlite)
library(tidyverse)

init_db <- function(dbpath = "curation.sqlite") {
  con <- dbConnect(SQLite(), dbpath)
  dbExecute(con, "
  CREATE TABLE IF NOT EXISTS studies (
    study_id TEXT PRIMARY KEY,
    title TEXT,
    species TEXT,
    contact TEXT,
    publications TEXT,
    source TEXT,
    added_at TEXT
  )")
  dbExecute(con, "
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
  )")
  con
}

upsert <- function(con, table, row, key) {
  dbExecute(con, sprintf("DELETE FROM %s WHERE %s = ?", table, key), params = list(row[[key]]))
  dbWriteTable(con, table, row, append = TRUE)
}

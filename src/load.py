
from pathlib import Path
from google.cloud import bigquery

# Configuration BigQuery
PROJECT_ID = "africanagriculturedatapipeline"
DATASET_ID = "agriculture_analytics"
TABLE_ID = "agriculture_processed"
LOCATION = "EU"

# Fichier transformé
FILE_PATH = Path("data/processed/agriculture_processed.parquet")


def load_to_bigquery():

    print("========== BIGQUERY LOAD ==========")

    if not FILE_PATH.exists():
        raise FileNotFoundError(f"Fichier introuvable : {FILE_PATH}")

    # Connexion à BigQuery avec les identifiants Google Cloud
    client = bigquery.Client(project=PROJECT_ID)

    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

    # Configuration du chargement Parquet
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
    )

    # Chargement du fichier
    with open(FILE_PATH, "rb") as parquet_file:
        job = client.load_table_from_file(
            parquet_file,
            table_ref,
            job_config=job_config,
            location=LOCATION
        )

    # Attendre la fin du chargement
    job.result()

    # Vérifier la table
    table = client.get_table(table_ref)

    print("\n========== LOAD TERMINÉ ==========")
    print(f"Table : {table_ref}")
    print(f"Lignes chargées : {table.num_rows}")
    print(f"Colonnes : {len(table.schema)}")


if __name__ == "__main__":
    load_to_bigquery()

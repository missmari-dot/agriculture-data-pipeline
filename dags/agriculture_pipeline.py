
from datetime import datetime, timedelta
from pathlib import Path
import subprocess

from airflow.sdk import dag, task


# Répertoire du projet dans le futur conteneur Airflow
PROJECT_DIR = Path("/opt/airflow/agriculture_pipeline")


def run_script(script_name: str):
    """Exécute un script Python du projet."""

    script_path = PROJECT_DIR / "src" / script_name

    if not script_path.exists():
        raise FileNotFoundError(
            f"Script introuvable : {script_path}"
        )

    subprocess.run(
        ["python", str(script_path)],
        cwd=str(PROJECT_DIR),
        check=True
    )


@dag(
    dag_id="agriculture_pipeline",
    description="African Agriculture Data Engineering Pipeline",
    schedule=None,
    start_date=datetime(2026, 11, 1),
    catchup=False,
    default_args={
        "owner": "agriculture_data_team",
        "retries": 1,
        "retry_delay": timedelta(minutes=2),
    },
    tags=["agriculture", "data-engineering", "bigquery"],
)
def agriculture_pipeline():

    @task
    def extract():
        run_script("extract.py")

    @task
    def validate_raw():
        run_script("validate.py")

    @task
    def transform():
        run_script("transform.py")

    @task
    def validate_processed():
        run_script("validate_processed.py")

    @task
    def load_to_bigquery():
        run_script("load.py")

    # Définition des dépendances
    extraction = extract()
    raw_validation = validate_raw()
    transformation = transform()
    processed_validation = validate_processed()
    loading = load_to_bigquery()

    extraction >> raw_validation >> transformation
    transformation >> processed_validation >> loading


agriculture_pipeline()

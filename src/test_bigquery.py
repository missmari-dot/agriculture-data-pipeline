
from google.cloud import bigquery

PROJECT_ID = "africanagriculturedatapipeline"

def test_connection():
    print("Connexion à BigQuery...")

    client = bigquery.Client(project=PROJECT_ID)

    query = """
        SELECT
            'African Agriculture Data Engineering Pipeline' AS project,
            'BigQuery Sandbox' AS environment,
            CURRENT_TIMESTAMP() AS execution_time,
            'SUCCESS' AS status
    """

    result = client.query(query, location="EU").result()

    for row in result:
        print("Projet :", row.project)
        print("Environnement :", row.environment)
        print("Exécution :", row.execution_time)
        print("Statut :", row.status)

    print("\nConnexion BigQuery réussie !")

if __name__ == "__main__":
    test_connection()

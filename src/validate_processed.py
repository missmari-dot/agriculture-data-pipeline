
import pandas as pd

FILE_PATH = "data/processed/agriculture_processed.parquet"


def validate_processed_data():
    df = pd.read_parquet(FILE_PATH)

    print("========== PROCESSED DATA VALIDATION ==========")

    checks = {
        "Nombre de lignes conservé": len(df) == 15000,
        "Clé unique": not df["record_key"].duplicated().any(),
        "Aucune valeur manquante": not df.isnull().any().any(),
        "Solde de production calculé": df["production_balance_kg"].notnull().all(),
        "Indicateur de rentabilité calculé": df["is_profitable"].notnull().all(),
        "Date de traitement présente": df["processed_at_utc"].notnull().all(),
    }

    for name, passed in checks.items():
        status = "PASS" if passed else "FAIL"
        print(f"{name}: [{status}]")

    print("\n========== STATISTIQUES ==========")
    print("Entreprises agricoles rentables :")
    print(df["is_profitable"].value_counts().to_string())

    print("\nSolde de production :")
    print(df["production_balance_kg"].value_counts().sort_index().to_string())

    if not all(checks.values()):
        raise ValueError("Certains contrôles ont échoué.")

    print("\nTous les contrôles sont réussis.")


if __name__ == "__main__":
    validate_processed_data()

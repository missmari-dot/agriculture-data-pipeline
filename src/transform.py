
import pandas as pd
from pathlib import Path

# Chemins des fichiers
RAW_FILE = Path("data/raw/agriculture_raw.parquet")
PROCESSED_FILE = Path("data/processed/agriculture_processed.parquet")


def transform_data():

    print("========== DATA TRANSFORMATION ==========")

    # 1. Charger les données brutes
    df = pd.read_parquet(RAW_FILE)

    print(f"Nombre de lignes chargées : {len(df)}")

    # 2. Créer une clé unique
    df["record_key"] = (
        df["source_file"].astype(str)
        + "_"
        + df["record_id"].astype(str)
    )

    # 3. Calculer le solde de production
    df["production_balance_kg"] = (
        df["total_production_kg"]
        - df["production_sold_kg"]
        - df["production_consumed_kg"]
    )

    # 4. Ajouter un indicateur de rentabilité
    df["is_profitable"] = df["net_income_usd"] > 0

    # 5. Ajouter la date de traitement en UTC
    df["processed_at_utc"] = pd.Timestamp.now(tz="UTC")

    # 6. Créer le dossier de destination
    PROCESSED_FILE.parent.mkdir(parents=True, exist_ok=True)

    # 7. Enregistrer les données transformées
    df.to_parquet(PROCESSED_FILE, index=False)

    print("\n========== TRANSFORMATION TERMINÉE ==========")
    print(f"Nombre de lignes : {len(df)}")
    print(f"Nombre de colonnes : {len(df.columns)}")
    print(f"Fichier généré : {PROCESSED_FILE}")

    print("\nAperçu des nouvelles colonnes :")
    print(
        df[
            [
                "record_key",
                "production_balance_kg",
                "is_profitable",
                "processed_at_utc"
            ]
        ].head()
    )

    return df


if __name__ == "__main__":
    transform_data()

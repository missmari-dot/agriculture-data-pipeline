
import pandas as pd

FILE_PATH = "data/raw/agriculture_raw.parquet"


def profile_data():
    df = pd.read_parquet(FILE_PATH)

    print("\n========== TYPES DE DONNÉES ==========")
    print(df.dtypes.to_string())

    print("\n========== STATISTIQUES NUMÉRIQUES ==========")
    print(df.describe().round(2).to_string())

    print("\n========== RÉPARTITION PAR SOURCE ==========")
    print(df["source_file"].value_counts().to_string())

    print("\n========== RÉPARTITION PAR PAYS ==========")
    print(df["country"].value_counts().to_string())

    print("\n========== RÉPARTITION DES CULTURES ==========")
    print(df["primary_crop"].value_counts().to_string())

    print("\n========== SCÉNARIOS ==========")
    print(df["scenario"].value_counts().to_string())

    print("\n========== VALEURS CATÉGORIELLES ==========")
    for column in ["farmer_gender", "farm_type", "soil_type", "season"]:
        print(f"\n{column}:")
        print(df[column].value_counts(dropna=False).to_string())


if __name__ == "__main__":
    profile_data()

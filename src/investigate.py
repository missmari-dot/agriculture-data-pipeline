
import pandas as pd

df = pd.read_parquet("data/raw/agriculture_raw.parquet")

# Calculer les quantités non expliquées
df["sold_consumed_total"] = (
    df["production_sold_kg"]
    + df["production_consumed_kg"]
)

df["production_difference_kg"] = (
    df["sold_consumed_total"]
    - df["total_production_kg"]
)

# Extraire les observations concernées
anomalies = df[
    df["production_difference_kg"] > 0.01
].copy()

print("========== ANALYSE DES INCOHÉRENCES ==========")

print("\nNombre d'anomalies :", len(anomalies))

print("\nStatistiques des dépassements :")
print(
    anomalies["production_difference_kg"]
    .describe()
    .round(2)
)

print("\nRépartition par scénario :")
print(anomalies["scenario"].value_counts())

print("\nRépartition par pays :")
print(anomalies["country"].value_counts())

print("\nExemples d'anomalies :")
columns = [
    "record_id",
    "country",
    "scenario",
    "total_production_kg",
    "production_sold_kg",
    "production_consumed_kg",
    "production_difference_kg"
]

print(anomalies[columns].head(15).to_string(index=False))

# Sauvegarder les observations à investiguer
anomalies[columns].to_csv(
    "data/production_anomalies.csv",
    index=False
)

print("\nRapport sauvegardé : data/production_anomalies.csv")

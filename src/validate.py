
import pandas as pd
from pathlib import Path

FILE_PATH = "data/raw/agriculture_raw.parquet"
REPORT_PATH = "data/validation_report.csv"

# Tolérance provisoire pour les écarts de production
TOLERANCE_KG = 1.0


def validate_data():
    df = pd.read_parquet(FILE_PATH)

    print("========== DATA QUALITY CHECKS ==========")
    print("Nombre de lignes :", len(df))

    results = []

    def add_check(name, condition, description):
        """Enregistre les observations qui ne respectent pas une règle."""

        invalid = df[condition.fillna(True)]

        status = "PASS" if invalid.empty else "WARNING"

        results.append({
            "check": name,
            "description": description,
            "invalid_rows": len(invalid),
            "status": status
        })

        print(f"\n{name}: {len(invalid)} anomalie(s) [{status}]")

        if not invalid.empty:
            columns = [
                col for col in [
                    "record_id",
                    "source_file",
                    "country",
                    "farm_size_ha",
                    "area_planted_ha",
                    "production_sold_kg",
                    "production_consumed_kg",
                    "total_production_kg",
                    "net_income_usd"
                ]
                if col in invalid.columns
            ]

            print(
                invalid[columns]
                .head(5)
                .to_string(index=False)
            )

    # ==========================================
    # 1. IDENTIFIANTS
    # ==========================================

    add_check(
        "Duplicate composite key",
        df.duplicated(
            subset=["source_file", "record_id"],
            keep=False
        ),
        "Unicité de source_file + record_id"
    )

    # ==========================================
    # 2. VALIDATION DES VALEURS NUMÉRIQUES
    # ==========================================

    add_check(
        "Invalid farmer age",
        (df["farmer_age"] < 15) | (df["farmer_age"] > 100),
        "Âge hors de la plage de contrôle 15-100 ans"
    )

    add_check(
        "Invalid farm size",
        df["farm_size_ha"] <= 0,
        "Superficie agricole nulle ou négative"
    )

    add_check(
        "Invalid planted area",
        df["area_planted_ha"] <= 0,
        "Superficie cultivée nulle ou négative"
    )

    add_check(
        "Invalid yield",
        df["yield_t_ha"] < 0,
        "Rendement négatif"
    )

    add_check(
        "Invalid rainfall",
        df["annual_rainfall_mm"] < 0,
        "Précipitations négatives"
    )

    # ==========================================
    # 3. COHÉRENCE DES SUPERFICIES
    # ==========================================

    add_check(
        "Planted area exceeds farm size",
        df["area_planted_ha"] > df["farm_size_ha"],
        "Surface cultivée supérieure à la surface totale"
    )

    # ==========================================
    # 4. COHÉRENCE DE LA PRODUCTION
    # ==========================================

    add_check(
        "Sold production exceeds total",
        df["production_sold_kg"] > df["total_production_kg"],
        "Production vendue supérieure à la production totale"
    )

    add_check(
        "Consumed production exceeds total",
        df["production_consumed_kg"] > df["total_production_kg"],
        "Production consommée supérieure à la production totale"
    )

    # Écart entre production totale et utilisation déclarée
    production_difference = (
        df["production_sold_kg"]
        + df["production_consumed_kg"]
        - df["total_production_kg"]
    )

    add_check(
        "Production balance exceeds tolerance",
        production_difference > TOLERANCE_KG + 1e-9,
        "Dépassement de production supérieur à 1 kg"
    )

    # ==========================================
    # 5. COHÉRENCE FINANCIÈRE
    # ==========================================

    add_check(
        "Invalid total cost",
        (
            (df["input_cost_usd"] < 0)
            | (df["labor_cost_usd"] < 0)
            | (df["total_cost_usd"] < 0)
        ),
        "Présence de coûts négatifs"
    )

    cost_difference = (
        df["total_cost_usd"]
        - df["input_cost_usd"]
        - df["labor_cost_usd"]
    ).abs()

    add_check(
        "Inconsistent total cost",
        cost_difference > 0.02,
        "Coût total différent de la somme des coûts"
    )

    net_income_difference = (
        df["net_income_usd"]
        - (df["revenue_usd"] - df["total_cost_usd"])
    ).abs()

    add_check(
        "Inconsistent net income",
        net_income_difference > 0.02,
        "Revenu net différent du revenu moins les coûts"
    )

    # ==========================================
    # 6. VALEURS SUSPECTES
    # ==========================================

    add_check(
        "Suspicious market distance",
        df["market_distance_km"] > 1000,
        "Distance au marché supérieure à 1000 km"
    )

    # ==========================================
    # 7. VALIDATION DES ANNÉES
    # ==========================================

    add_check(
        "Invalid year",
        (df["year"] < 2018) | (df["year"] > 2025),
        "Année en dehors de la période attendue"
    )

    # ==========================================
    # 8. RAPPORT FINAL
    # ==========================================

    report = pd.DataFrame(results)

    print("\n========== RÉSUMÉ DES VALIDATIONS ==========")

    print(
        report[
            ["check", "invalid_rows", "status"]
        ].to_string(index=False)
    )

    # Créer le dossier si nécessaire
    Path("data").mkdir(parents=True, exist_ok=True)

    report.to_csv(REPORT_PATH, index=False)

    print(f"\nRapport sauvegardé : {REPORT_PATH}")

    return report


if __name__ == "__main__":
    validate_data()

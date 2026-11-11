
import os
from pathlib import Path

# Déplacer le cache Hugging Face vers D:
os.environ["HF_HOME"] = "D:/HF-Cache"
os.environ["HF_HUB_CACHE"] = "D:/HF-Cache/hub"

import pandas as pd
from huggingface_hub import HfApi, hf_hub_download

DATASET_ID = (
    "electricsheepafrica/"
    "africa-synth-agriculture-smallholder-crop-yields-africa-all"
)


def extract_data():
    print("Téléchargement du dataset agricole depuis Hugging Face...")

    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Récupérer la liste des fichiers du dataset
    api = HfApi()
    files = api.list_repo_files(
        repo_id=DATASET_ID,
        repo_type="dataset"
    )

    csv_files = [
        file for file in files
        if file.lower().endswith(".csv")
    ]

    if not csv_files:
        raise ValueError("Aucun fichier CSV trouvé dans le dataset.")

    print(f"\nNombre de fichiers CSV trouvés : {len(csv_files)}")

    dataframes = []

    for filename in csv_files:
        print(f"\nTéléchargement : {filename}")

        file_path = hf_hub_download(
            repo_id=DATASET_ID,
            filename=filename,
            repo_type="dataset",
            cache_dir="D:/HF-Cache/hub"
        )

        df_part = pd.read_csv(file_path)

        # Conserver la provenance de chaque ligne
        df_part["source_file"] = Path(filename).name

        print(f"Nombre de lignes : {len(df_part)}")
        dataframes.append(df_part)

    # Regrouper les fichiers CSV
    df = pd.concat(dataframes, ignore_index=True)

    print("\nExtraction terminée !")
    print("Nombre total de lignes :", df.shape[0])
    print("Nombre de colonnes :", df.shape[1])

    print("\nColonnes disponibles :")
    print(df.columns.tolist())

    print("\nAperçu des données :")
    print(df.head())

    print("\nInformations sur les données :")
    df.info()

    # Sauvegarder les données brutes au format Parquet
    output_file = output_dir / "agriculture_raw.parquet"
    df.to_parquet(output_file, index=False)

    print(f"\nFichier brut sauvegardé : {output_file}")

    return df


if __name__ == "__main__":
    extract_data()

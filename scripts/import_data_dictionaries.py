from pathlib import Path

from src.importer.data_dict import SectorDictImporter, ThemeDictImporter
from src.db.db_handler import DBHandler


def main():

    # Instantiate DB Handler and data dictionary importers
    db_handler = DBHandler()
    importers = [SectorDictImporter(db_handler), ThemeDictImporter(db_handler)]

    # Set file paths to data dictionary files
    base_path = Path(".") / "data" / "dictionary"
    file_paths = [base_path / "sector_dict.csv", base_path / "theme_dict.csv"]

    # Dynamically populate data dictionaries
    for importer, file_path in zip(importers, file_paths):
        print(f"Importing data for {importer.table_class.__name__}...")
        importer.import_csv(file_path)


if __name__ == "__main__":
    main()

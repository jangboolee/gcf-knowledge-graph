from pathlib import Path

from src.importer.export import CountryExportImporter
from src.db.db_handler import DBHandler


def main():

    # Instantiate DB Handler and data export importers
    db_handler = DBHandler()
    importers = [
        CountryExportImporter(db_handler),
    ]

    # Set file paths to data export files
    base_path = Path(".") / "data" / "export"
    file_paths = [base_path / "country.xlsx"]

    # Dynamically populate data export tables
    for importer, file_path in zip(importers, file_paths):
        print(f"Importing data for {importer.table_class.__name__}...")
        importer.import_xlsx(file_path)
        print("\n")


if __name__ == "__main__":

    main()

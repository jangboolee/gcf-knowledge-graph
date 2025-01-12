from pathlib import Path

from src.importer.data_dict import (
    ActivityTypeDictImporter,
    EntityTypeDictImporter,
    EssCategoryDictImporter,
    ModalityDictImporter,
    ProjectSizeDictImporter,
    ReadinessStatusDictImporter,
    RegionDictImporter,
    SectorDictImporter,
    StageDictImporter,
    ThemeDictImporter,
)
from src.db.db_handler import DBHandler


def main():

    # Instantiate DB Handler and data dictionary importers
    db_handler = DBHandler()
    importers = [
        ActivityTypeDictImporter(db_handler),
        EntityTypeDictImporter(db_handler),
        EssCategoryDictImporter(db_handler),
        ModalityDictImporter(db_handler),
        ProjectSizeDictImporter(db_handler),
        ReadinessStatusDictImporter(db_handler),
        RegionDictImporter(db_handler),
        SectorDictImporter(db_handler),
        StageDictImporter(db_handler),
        ThemeDictImporter(db_handler),
    ]

    # Set file paths to data dictionary files
    base_path = Path(".") / "data" / "dictionary"
    file_paths = [
        base_path / "activity_type_dict.csv",
        base_path / "entity_type_dict.csv",
        base_path / "ess_category_dict.csv",
        base_path / "modality_dict.csv",
        base_path / "project_size_dict.csv",
        base_path / "readiness_status_dict.csv",
        base_path / "region_dict.csv",
        base_path / "sector_dict.csv",
        base_path / "stage_dict.csv",
        base_path / "theme_dict.csv",
    ]

    # Dynamically populate data dictionaries
    for importer, file_path in zip(importers, file_paths):
        print(f"Importing data for {importer.table_class.__name__}...")
        importer.import_csv(file_path)
        print("\n")


if __name__ == "__main__":

    main()

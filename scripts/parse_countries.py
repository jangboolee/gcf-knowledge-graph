from pathlib import Path

from src.parser import ProjectCountryParser, ReadinessCountryParser
from src.db.db_handler import DBHandler


def main():

    # Instantiate DB Handler and country parsers
    db_handler = DBHandler()
    parsers = [
        ProjectCountryParser(db_handler),
        ReadinessCountryParser(db_handler),
    ]

    # Set file paths to data export files
    base_path = Path(".") / "data" / "export"
    file_paths = [
        base_path / "project.xlsx",
        base_path / "readiness.xlsx",
    ]

    # Dynamically parse countries from data export tables
    for parser, file_path in zip(parsers, file_paths):
        print(f"Parsing countries from {parser.table_class.__name__}...")
        parser.parse_countries(file_path)
        print("\n")


if __name__ == "__main__":

    main()

import logging
from typing import Type

import pandas as pd
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import DeclarativeMeta
import country_converter as coco

from src.db.db_handler import DBHandler
from src.db.db_schema import CountryDict


class BaseCountryParser:

    def __init__(
        self,
        db_handler: DBHandler,
        table_class: Type[DeclarativeMeta],
    ) -> None:
        self.db_handler = db_handler
        self.table_class = table_class
        # Instance variable to save class-specific inputs
        self.country_col = None
        self.final_cols = None
        # Instance variable to save ISO3 to country_id mapper
        self.country_id_mapper = None
        # Country converter instance for country name matching
        self.cc = coco.CountryConverter()
        # Instance variables to save dataframes
        self.input = None
        self.parsed = None
        # Run helper to get country ID mapper
        self._get_country_id_mapper()

    def _get_country_id_mapper(self) -> bool:
        """Helper to get a ISO3 to country ID mapper

        Returns:
            bool: True after completion
        """

        # Create name to ID mapping dictionary
        with self.db_handler.get_session() as session:
            mapper = {
                item.iso3: item.id for item in session.query(CountryDict).all()
            }

        # Assign the mapper to the corresponding instance variable
        self.country_id_mapper = mapper

        return True

    def _read_xlsx(self, file_path: str) -> bool:
        """Helper method to read in an XLSX data export file as a dataframe,
        create a new ID column, and retrieve only the country name column for
        country parsing

        Args:
            file_path (str): Path to the Excel data export file

        Raises:
            ValueError: Raise error if reading doesn't work

        Returns:
            bool: True if successful, False if not
        """

        try:
            df = pd.read_excel(file_path)
            df["id"] = range(1, len(df) + 1)
            self.input = df[["id", self.country_col]]
            return True
        except Exception as e:
            raise ValueError(f"Error reading XLSX file at {file_path}: {e}")
        return False

    def _explode_country_names(self) -> bool:
        """Helper to split and explode country names per row

        Returns:
            bool: True after completion
        """

        df = self.input

        # Split strings of country names into lists of country names
        df[self.country_col] = df[self.country_col].str.split(", ")
        # Explode each list to the row-level
        df = df.explode(self.country_col, ignore_index=True)

        self.parsed = df

        return True

    def _map_country_ids(self) -> bool:
        """Map ISO3 from country name, then map country ID from ISO3

        Returns:
            bool: True after completion
        """

        df = self.parsed

        # Map ISO3 from country names using country converter
        df["iso3"] = self.cc.pandas_convert(df["Countries"])
        # Map country ID from ISO3 using custom mapper
        df["country_id"] = df["iso3"].map(self.country_id_mapper)
        # Drop redundant columns
        df.drop([self.country_col, "iso3"], axis=1, inplace=True)

        self.parsed = df

        return True

    def _write_to_db(self) -> bool:
        """Helper method to write a Pandas dataframe as a table in the DB

        Returns:
            bool: True if successful, False if not
        """

        df = self.parsed

        with self.db_handler.get_session() as session:
            try:
                records = df.to_dict(orient="records")
                session.bulk_insert_mappings(self.table_class, records)
                session.commit()
                print(
                    f"Inserted {len(records)} records into "
                    f"{self.table_class.__tablename__}."
                )
                return True
            except IntegrityError as e:
                session.rollback()
                logging.error(f"IntegrityError: {e}")
            except Exception as e:
                session.rollback()
                logging.error(f"Failed to write data to the database: {e}")

        return False

    def parse_country(self, file_path: str) -> bool:
        """High-level main method to parse out multiple country values in a
        single cell to multiple rows

        Args:
            file_path (str): Path to the XLSX file

        Returns:
            bool: True if successful, False if not
        """

        self._read_xlsx(file_path)
        self._explode_country_names()
        self._map_country_ids()
        self.parsed.columns = self.final_cols

        return self._write_to_db()

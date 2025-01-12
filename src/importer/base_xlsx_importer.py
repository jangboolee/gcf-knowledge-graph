import logging

import pandas as pd
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import DeclarativeMeta
from typing import Type

from src.db.db_handler import DBHandler


class BaseXlsxImporter:

    def __init__(
        self, db_handler: DBHandler, table_class: Type[DeclarativeMeta]
    ) -> None:
        self.db_handler = db_handler
        self.table_class = table_class
        self.cols = [
            col.name
            for col in self.table_class.__table__.columns
            if col.name != "id"
        ]

    def _read_xlsx(self, file_path: str) -> pd.DataFrame:
        """Helper method to read in an XLSX data export file as a dataframe

        Args:
            file_path (str): Path to the Excel data export file

        Raises:
            ValueError: Raise error if reading doesn't work

        Returns:
            pd.DataFrame: Contents of the XLSX file as a Pandas dataframe
        """

        try:
            return pd.read_excel(file_path)
        except Exception as e:
            raise ValueError(f"Error reading XLSX file at {file_path}: {e}")

    def _process_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """Abstract method to process the dataframe, namely:
            1. Drop any calculated columns
            2. Replace names with IDs
            3. Align column names with the schema

        Args:
            df (pd.DataFrame): Dataframe of the export file, read-as-is

        Raises:
            NotImplementedError: Raises error if called directly within the
                abstract base class

        Returns:
            pd.DataFrame: Processed dataframe
        """

        raise NotImplementedError

    def _write_to_db(self, df: pd.DataFrame) -> bool:
        """Helper method to write a Pandas dataframe as a table in the DB

        Args:
            df (pd.DataFrame): Contents of CSV file read in as a dataframe,
                after processing

        Returns:
            bool: True if successful, False if not
        """

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

    def import_xlsx(self, file_path: str) -> bool:
        """High-level main method to import a XLSX data export file into the
        database

        Args:
            file_path (str): Path to the CSV file

        Returns:
            bool: True if successful, False if not
        """

        raw = self._read_xlsx(file_path)
        processed = self._process_df(raw)
        return self._write_to_db(processed)

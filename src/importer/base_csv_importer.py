import logging

import pandas as pd
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import DeclarativeMeta
from typing import Type

from src.db.db_handler import DBHandler


class BaseCsvImporter:

    def __init__(
        self, db_handler: DBHandler, table_class: Type[DeclarativeMeta]
    ) -> None:
        self.db_handler = db_handler
        self.table_class = table_class

    def _read_csv(self, file_path: str) -> pd.DataFrame:
        """Helper method to read a CSV file as a Pandas dataframe

        Args:
            file_path (str): Path to the CSV file

        Raises:
            ValueError: Raise error if reading doesn't work

        Returns:
            pd.DataFrame: Contents of the CSV file as a Pandas dataframe
        """

        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise ValueError(f"Error reading CSV file at {file_path}: {e}")

    def _write_to_db(self, df: pd.DataFrame) -> bool:
        """Helper method to write a Pandas dataframe as a table in the DB

        Args:
            df (pd.DataFrame): Contents of CSV file read in as a dataframe

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

    def import_csv(self, file_path: str) -> bool:
        """High-level main method to import a CSV into the database

        Args:
            file_path (str): Path to the CSV file

        Returns:
            bool: True if successful, False if not
        """

        df = self._read_csv(file_path)
        return self._write_to_db(df)

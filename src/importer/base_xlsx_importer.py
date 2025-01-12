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

    def _get_id_mapper(self, table_class: Type[DeclarativeMeta]) -> bool:
        """General helper to get a name to ID mapper for any given table class

        Args:
            table_class (Type[DeclarativeMeta]): The SQLAlchemy ORM table class

        Returns:
            bool: True after completion.
        """

        # Create name to ID mapping dictionary
        with self.db_handler.get_session() as session:
            mapper = {
                getattr(item, "name"): getattr(item, "id")
                for item in session.query(table_class).all()
            }

        # Assign the mapper to the corresponding instance variable
        var_name = f"{table_class.__name__.lower().replace('dict', '')}"
        setattr(self, f"{var_name}_id_mapper", mapper)

        return True

    def _map_ids(
        self,
        df: pd.DataFrame,
        name_col: str,
        id_col: str,
        mapper: dict[str, int],
    ) -> bool:
        """Helper to map the IDs from the names, and then drop the name column

        Args:
            df (pd.DataFrame): Dataframe to map IDs on
            name_col (str): Name of the column with names to map from
            id_col (str): Name of the ID column to map to
            mapper (dict[str, int]): Mapper with name as key and id as value

        Returns:
            bool: True after completion
        """

        # Map the ID from the names, using the mapper
        df[id_col] = df[name_col].map(mapper)
        # Drop the redundant name column
        df.drop(name_col, axis=1, inplace=True)

        return True

    def _move_col(
        self, df: pd.DataFrame, col_name: str, insert_idx: int
    ) -> bool:
        """Helper to move a column to a desired location within a dataframe

        Args:
            df (pd.DataFrame): Dataframe to use for moving columns
            col_name (str): Name of the column to move
            insert_idx (int): Column index to insert the column into

        Returns:
            bool: True if successful, False if not
        """

        if col_name in df.columns:
            move_series = df.pop(col_name)
            df.insert(insert_idx, col_name, move_series)
            return True

        return False

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

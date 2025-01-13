import pandas as pd

from src.importer.base_xlsx_importer import BaseXlsxImporter
from src.db.db_handler import DBHandler
from src.db.db_schema import (
    Entity,
    CountryDict,
    EntityTypeDict,
    StageDict,
    SizeDict,
    SectorDict,
)


class EntityExportImporter(BaseXlsxImporter):

    def __init__(self, db_handler: DBHandler) -> None:
        super().__init__(db_handler=db_handler, table_class=Entity)
        self.country_id_mapper = None
        self.entitytype_id_mapper = None
        self.stage_id_mapper = None
        self.size_id_mapper = None
        self.sector_id_mapper = None

    def _get_country_id_mapper(self) -> bool:
        """Helper getter to get the region name to ID mapper

        Returns:
            bool: True after completion
        """
        return self._get_id_mapper(CountryDict)

    def _get_entity_type_id_mapper(self) -> bool:
        """Helper getter to get the entity type name to ID mapper

        Returns:
            bool: True after completion
        """

        return self._get_id_mapper(EntityTypeDict)

    def _get_stage_id_mapper(self) -> bool:
        """Helper getter to get the stage name to ID mapper

        Returns:
            bool: True after completion
        """

        return self._get_id_mapper(StageDict)

    def _get_size_id_mapper(self) -> bool:
        """Helper getter to get the size name to ID mapper

        Returns:
            bool: True after completion
        """

        return self._get_id_mapper(SizeDict)

    def _get_sector_id_mapper(self) -> bool:
        """Helper getter to get the sector name to ID mapper

        Returns:
            bool: True after completion
        """

        return self._get_id_mapper(SectorDict)

    def _process_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """Overridden helper method to process the Entity data export file

        Args:
            df (pd.DataFrame): Raw dataframe of the Entity data export file

        Returns:
            pd.DataFrame: Processed dataframe of Entity data
        """

        # Drop the 2 calculated columns
        df = df.iloc[:, :-2]
        # Get mapper to map region ID from region name
        self._get_country_id_mapper()
        self._get_entity_type_id_mapper()
        self._get_stage_id_mapper()
        self._get_sector_id_mapper()
        self._get_size_id_mapper()
        # Reconcile country naming differences
        self.country_id_mapper["United States"] = 236
        self.country_id_mapper["Philippines (the)"] = 176
        self.country_id_mapper["Cote d'Ivoire"] = 55
        self.country_id_mapper["Venezuela (Bolivarian Republic of)"] = 176
        self.country_id_mapper["Bolivia (Plurinational State of)"] = 241
        self.country_id_mapper["United Kingdom"] = 235
        self.country_id_mapper["Tanzania"] = 220
        self.country_id_mapper["Netherlands (the)"] = 157
        self.country_id_mapper["Micronesia (Federated States of)"] = 145
        # Trim leading whitespaces
        self.country_id_mapper["Republic of Korea (the)"] = 176
        df["Size"] = df["Size"].str.lstrip()
        # Remove "B." string from BM columns while keeping NaN values
        df["BM"] = (
            df["BM"]
            .str.removeprefix("B.")
            .pipe(pd.to_numeric, errors="coerce")
        )
        # Map IDs from names
        self._map_ids(df, "Country", "country_id", self.country_id_mapper)
        self._map_ids(df, "Type", "entity_type_id", self.entitytype_id_mapper)
        self._map_ids(df, "Stage", "stage_id", self.stage_id_mapper)
        self._map_ids(df, "Size", "size_id", self.size_id_mapper)
        self._map_ids(df, "Sector", "sector_id", self.sector_id_mapper)
        # Move ID columns
        self._move_col(df, "country_id", 2)
        self._move_col(df, "entity_type_id", 4)
        self._move_col(df, "stage_id", 5)
        self._move_col(df, "size_id", 7)
        self._move_col(df, "sector_id", 8)
        # Rename columns
        df.columns = self.cols

        return df

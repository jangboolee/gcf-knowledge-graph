import pandas as pd

from src.importer.base_xlsx_importer import BaseXlsxImporter
from src.db.db_handler import DBHandler
from src.db.db_schema import (
    Entity,
    CountryDict,
    EntityTypeDict,
    StageDict,
    BmDict,
    SizeDict,
    SectorDict,
)


class EntityExportImporter(BaseXlsxImporter):

    def __init__(self, db_handler: DBHandler) -> None:
        super().__init__(db_handler=db_handler, table_class=Entity)
        self.country_id_mapper = None
        self.entitytype_id_mapper = None
        self.stage_id_mapper = None
        self.bm_id_mapper = None
        self.size_id_mapper = None
        self.sector_id_mapper = None

    def _get_all_mappers(self) -> bool:
        """Overriden helper method to get all required mappers for importing
        the Entity export file

        Returns:
            bool: True if all getters are successful, False if not
        """

        return all(
            [
                self._get_id_mapper(CountryDict, name_col="iso3"),
                self._get_id_mapper(EntityTypeDict),
                self._get_id_mapper(StageDict),
                self._get_id_mapper(BmDict),
                self._get_id_mapper(SizeDict),
                self._get_id_mapper(SectorDict),
            ]
        )

    def _process_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """Overridden helper method to process the Entity data export file

        Args:
            df (pd.DataFrame): Raw dataframe of the Entity data export file

        Returns:
            pd.DataFrame: Processed dataframe of Entity data
        """

        # Drop the 2 calculated columns
        df = df.iloc[:, :-2]
        # Get all mappers for importing entity export file
        self._get_all_mappers()
        # Use country_converter to map ISO3 from country names and drop names
        df["iso3"] = self.cc.pandas_convert(series=df["Country"], to="ISO3")
        df.drop("Country", axis=1, inplace=True)
        # Trim leading whitespaces
        df["Size"] = df["Size"].str.lstrip()
        # Map IDs from names
        self._map_ids(df, "iso3", "country_id", self.country_id_mapper)
        self._map_ids(df, "Type", "entity_type_id", self.entitytype_id_mapper)
        self._map_ids(df, "Stage", "stage_id", self.stage_id_mapper)
        self._map_ids(df, "BM", "bm_id", self.bm_id_mapper)
        self._map_ids(df, "Size", "size_id", self.size_id_mapper)
        self._map_ids(df, "Sector", "sector_id", self.sector_id_mapper)
        # Move ID columns
        self._move_col(df, "country_id", 2)
        self._move_col(df, "entity_type_id", 4)
        self._move_col(df, "stage_id", 5)
        self._move_col(df, "bm_id", 6)
        self._move_col(df, "size_id", 7)
        self._move_col(df, "sector_id", 8)
        # Rename columns
        df.columns = self.cols

        return df

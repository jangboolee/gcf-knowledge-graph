import pandas as pd

from src.importer.base_xlsx_importer import BaseXlsxImporter
from src.db.db_handler import DBHandler
from src.db.db_schema import (
    Project,
    ModalityDict,
    Entity,
    BmDict,
    SectorDict,
    ThemeDict,
    SizeDict,
    EssCategoryDict,
)


class ProjectExportImporter(BaseXlsxImporter):

    def __init__(self, db_handler: DBHandler) -> None:
        super().__init__(db_handler=db_handler, table_class=Project)
        self.modality_id_mapper = None
        self.entity_id_mapper = None
        self.bm_id_mapper = None
        self.sector_id_mapper = None
        self.theme_id_mapper = None
        self.size_id_mapper = None
        self.esscategory_id_mapper = None

    def _get_all_mappers(self) -> bool:
        """Overriden helper method to get all required mappers for importing
        the Project export file

        Returns:
            bool: True if all getters are successful, False if not
        """

        return all(
            [
                self._get_id_mapper(ModalityDict),
                self._get_id_mapper(Entity, name_col="code"),
                self._get_id_mapper(BmDict),
                self._get_id_mapper(SectorDict),
                self._get_id_mapper(ThemeDict),
                self._get_id_mapper(SizeDict),
                self._get_id_mapper(EssCategoryDict),
            ]
        )

    def _process_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """Overridden helper method to process the Country data export file

        Args:
            df (pd.DataFrame): Raw dataframe of the Country data export file

        Returns:
            pd.DataFrame: Processed dataframe of Country data
        """

        # Drop Countries column with multiple values per cell
        df.drop("Countries", axis=1, inplace=True)
        # Get all mappers to map ID from name
        self._get_all_mappers()
        # Map IDs using names
        self._map_ids(df, "Modality", "modality_id", self.modality_id_mapper)
        self._map_ids(df, "Entity", "entity_id", self.entity_id_mapper)
        self._map_ids(df, "BM", "bm_id", self.bm_id_mapper)
        self._map_ids(df, "Sector", "sector_id", self.sector_id_mapper)
        self._map_ids(df, "Theme", "theme_id", self.theme_id_mapper)
        self._map_ids(df, "Project Size", "size_id", self.size_id_mapper)
        self._map_ids(
            df, "ESS Category", "ess_category_id", self.esscategory_id_mapper
        )
        # Re-arrange columns
        self._move_col(df, "modality_id", 1)
        self._move_col(df, "entity_id", 3)
        self._move_col(df, "entity_id", 4)
        self._move_col(df, "FA Financing", 9)
        # Rename columns
        df.columns = self.cols

        return df

import pandas as pd

from src.importer.base_xlsx_importer import BaseXlsxImporter
from src.db.db_handler import DBHandler
from src.db.db_schema import Country, RegionDict


class CountryExportImporter(BaseXlsxImporter):

    def __init__(self, db_handler: DBHandler) -> None:
        super().__init__(db_handler=db_handler, table_class=Country)
        self.region_id_mapper = None

    def _get_region_id_mapper(self) -> bool:
        """Helper getter to get the region name to ID mapper

        Returns:
            bool: True after completion
        """

        return self._get_id_mapper(RegionDict)

    def _process_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """Overridden helper method to process the Country data export file

        Args:
            df (pd.DataFrame): Raw dataframe of the Country data export file

        Returns:
            pd.DataFrame: Processed dataframe of Country data
        """

        # Drop the 4 calculated columns
        df = df.iloc[:, :-4]
        # Get mapper to map region ID from region name
        self._get_region_id_mapper()
        # Map region name with region ID
        self._map_ids(df, "Region", "region_id", self.region_id_mapper)
        # Move region ID column to the 3rd column
        self._move_col(df, "region_id", 2)
        # Rename columns
        df.columns = self.cols

        return df

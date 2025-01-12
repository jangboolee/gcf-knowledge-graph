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
        processed = df.iloc[:, :-4]
        # Get mapper to map region ID from region name
        self._get_region_id_mapper()
        # Map region name with region ID
        processed["region_id"] = processed["Region"].map(self.region_id_mapper)
        # Drop region name
        processed.drop("Region", axis=1, inplace=True)
        # Move region ID column to the 3rd column
        region_id_series = processed.pop("region_id")
        processed.insert(2, "region_id", region_id_series)
        # Rename columns
        processed.columns = self.cols

        return processed

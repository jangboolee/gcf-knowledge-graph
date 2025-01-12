import pandas as pd

from src.importer.base_xlsx_importer import BaseXlsxImporter
from src.db.db_handler import DBHandler
from src.db.db_schema import Country, RegionDict


class CountryExportImporter(BaseXlsxImporter):

    def __init__(self, db_handler: DBHandler) -> None:
        super().__init__(db_handler=db_handler, table_class=Country)
        self.region_id_mapper = None

    def _get_region_id_mapper(self) -> bool:

        # Create region name to ID mapping dictionary
        with self.db_handler.get_session() as session:
            mapper = {
                region.name: region.id
                for region in session.query(
                    RegionDict.name, RegionDict.id
                ).all()
            }
        self.region_id_mapper = mapper

        return True

    def _process_df(self, df: pd.DataFrame) -> pd.DataFrame:

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

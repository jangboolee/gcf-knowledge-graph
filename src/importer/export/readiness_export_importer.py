import pandas as pd

from src.importer.base_xlsx_importer import BaseXlsxImporter
from src.db.db_handler import DBHandler
from src.db.db_schema import (
    Readiness,
    ActivityTypeDict,
    DeliveryPartnerDict,
    RegionDict,
    StatusDict,
)


class ReadinessExportImporter(BaseXlsxImporter):

    def __init__(self, db_handler: DBHandler) -> None:
        super().__init__(db_handler=db_handler, table_class=Readiness)
        self.activitytype_id_mapper = None
        self.deliverypartner_id_mapper = None
        self.region_id_mapper = None
        self.status_id_mapper = None

    def _get_all_mappers(self) -> bool:
        """Overriden helper method to get all required mappers for importing
        the Readiness export file

        Returns:
            bool: True if all getters are successful, False if not
        """

        return all(
            [
                self._get_id_mapper(ActivityTypeDict),
                self._get_id_mapper(DeliveryPartnerDict),
                self._get_id_mapper(RegionDict, name_col="code"),
                self._get_id_mapper(StatusDict),
            ]
        )

    def _process_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """Overridden helper method to process the Country data export file

        Args:
            df (pd.DataFrame): Raw dataframe of the Country data export file

        Returns:
            pd.DataFrame: Processed dataframe of Country data
        """

        # Drop Country column with multiple values per cell
        df.drop("Country", axis=1, inplace=True)
        # Get mapper to map region ID from region name
        self._get_all_mappers()
        # Strip trailing whitespace from Delivery Partner
        df["Delivery Partner"] = df["Delivery Partner"].str.rstrip()
        # Map IDs using names
        self._map_ids(
            df, "Activity", "activity_type_id", self.activitytype_id_mapper
        )
        self._map_ids(
            df,
            "Delivery Partner",
            "delivery_partner_id",
            self.deliverypartner_id_mapper,
        )
        self._map_ids(df, "Region", "region_id", self.region_id_mapper)
        self._map_ids(df, "Status", "status_id", self.status_id_mapper)
        # Re-arrange column order
        self._move_col(df, "activity_type_id", 1)
        self._move_col(df, "delivery_partner_id", 3)
        self._move_col(df, "region_id", 4)
        self._move_col(df, "status_id", 8)
        # Convert approve date to datetime object
        df["Approved Date"] = pd.to_datetime(
            df["Approved Date"], format="%b %d, %Y"
        ).dt.date
        # Rename columns
        df.columns = self.cols

        return df

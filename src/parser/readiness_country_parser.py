from src.parser.base_country_parser import BaseCountryParser
from src.db.db_handler import DBHandler
from src.db.db_schema import ReadinessCountry


class ReadinessCountryParser(BaseCountryParser):

    def __init__(self, db_handler: DBHandler) -> None:
        super().__init__(db_handler=db_handler, table_class=ReadinessCountry)
        self.country_col = "Country"
        self.final_cols = ["readiness_id", "country_id"]

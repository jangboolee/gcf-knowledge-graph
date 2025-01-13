from src.parser.base_country_parser import BaseCountryParser
from src.db.db_handler import DBHandler
from src.db.db_schema import ProjectCountry


class ProjectCountryParser(BaseCountryParser):

    def __init__(self, db_handler: DBHandler) -> None:
        super().__init__(db_handler=db_handler, table_class=ProjectCountry)
        self.country_col = "Countries"
        self.final_cols = ["project_id", "country_id"]

from src.importer.base_csv_importer import BaseCsvImporter
from src.db.db_handler import DBHandler
from src.db.db_schema import ReadinessStatusDict


class ReadinessStatusDictImporter(BaseCsvImporter):

    def __init__(self, db_handler: DBHandler) -> None:
        super().__init__(
            db_handler=db_handler, table_class=ReadinessStatusDict
        )

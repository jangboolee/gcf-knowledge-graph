from neo4j import Session

from src.kg.services.base_meta_service import MetaService
from src.db.db_schema import SectorDict


class SectorService(MetaService):

    def __init__(self, session: Session) -> None:

        super().__init__(session, SectorDict)
        self.node_label = "Sector"

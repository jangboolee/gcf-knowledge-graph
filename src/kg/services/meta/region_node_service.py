from neo4j import Session


from src.kg.services.base_meta_service import MetaService
from src.db.db_schema import RegionDict


class RegionService(MetaService):

    def __init__(self, session: Session) -> None:

        super().__init__(session, RegionDict)
        self.node_label = "Region"

from neo4j import Session

from src.kg.services.base_meta_service import MetaService
from src.db.db_schema import EntityTypeDict


class EntityTypeService(MetaService):

    def __init__(self, session: Session) -> None:

        super().__init__(session, EntityTypeDict)
        self.node_label = "EntityType"

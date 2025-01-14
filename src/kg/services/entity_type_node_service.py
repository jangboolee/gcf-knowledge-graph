from neo4j import Session

from src.kg.services.base_node_service import NodeService
from src.db.db_schema import EntityTypeDict


class EntityTypeService(NodeService):

    def __init__(self, session: Session) -> None:

        super().__init__(session, EntityTypeDict)
        self.node_label = "EntityType"

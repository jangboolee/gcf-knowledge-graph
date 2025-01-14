from src.kg.services.nodes.base_node_service import NodeService
from src.db.db_schema import EntityTypeDict

from neo4j import Session


class EntityTypeService(NodeService):

    def __init__(self, session: Session) -> None:

        super().__init__(session, EntityTypeDict)
        self.node_label = "EntityType"

from src.kg.services.base_node_service import NodeService
from src.db.db_schema import SizeDict

from neo4j import Session


class SizeService(NodeService):

    def __init__(self, session: Session) -> None:

        super().__init__(session, SizeDict)
        self.node_label = "Size"

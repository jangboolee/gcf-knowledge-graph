from neo4j import Session

from src.kg.services.base_node_service import NodeService
from src.db.db_schema import StatusDict


class StatusService(NodeService):

    def __init__(self, session: Session) -> None:

        super().__init__(session, StatusDict)
        self.node_label = "Status"

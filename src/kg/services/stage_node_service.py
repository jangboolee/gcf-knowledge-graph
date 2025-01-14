from src.kg.services.base_node_service import NodeService
from src.db.db_schema import StageDict

from neo4j import Session


class StageService(NodeService):

    def __init__(self, session: Session) -> None:

        super().__init__(session, StageDict)
        self.node_label = "Stage"

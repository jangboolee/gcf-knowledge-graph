from src.kg.services.base_node_service import NodeService
from src.db.db_schema import ThemeDict

from neo4j import Session


class ThemeService(NodeService):

    def __init__(self, session: Session) -> None:

        super().__init__(session, ThemeDict)
        self.node_label = "Theme"

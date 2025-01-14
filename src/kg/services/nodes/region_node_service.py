from src.kg.services.nodes.base_node_service import NodeService
from src.db.db_handler import DBHandler
from src.db.db_schema import RegionDict

from neo4j import Session


class RegionService(NodeService):

    def __init__(self, session: Session) -> None:

        super().__init__(DBHandler(), session, RegionDict)
        self.node_label = "Region"

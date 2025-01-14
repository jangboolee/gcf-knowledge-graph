from src.kg.services.nodes.base_node_service import NodeService
from src.db.db_schema import ModalityDict

from neo4j import Session


class ModalityService(NodeService):

    def __init__(self, session: Session) -> None:

        super().__init__(session, ModalityDict)
        self.node_label = "Modality"

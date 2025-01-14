from src.kg.services.base_node_service import NodeService
from src.db.db_schema import EssCategoryDict

from neo4j import Session


class EssCategoryService(NodeService):

    def __init__(self, session: Session) -> None:

        super().__init__(session, EssCategoryDict)
        self.node_label = "EssCategory"

from neo4j import Session

from src.kg.services.base_meta_service import MetaService
from src.db.db_schema import ModalityDict


class ModalityService(MetaService):

    def __init__(self, session: Session) -> None:

        super().__init__(session, ModalityDict)
        self.node_label = "Modality"

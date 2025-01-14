from neo4j import Session

from src.kg.services.base_meta_service import MetaService
from src.db.db_schema import ActivityTypeDict


class ActivityTypeService(MetaService):

    def __init__(self, session: Session) -> None:

        super().__init__(session, ActivityTypeDict)
        self.node_label = "ActivityType"

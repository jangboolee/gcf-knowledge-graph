from src.kg.services.base_node_service import NodeService
from src.db.db_schema import ActivityTypeDict

from neo4j import Session


class ActivityTypeService(NodeService):

    def __init__(self, session: Session) -> None:

        super().__init__(session, ActivityTypeDict)
        self.node_label = "ActivityType"

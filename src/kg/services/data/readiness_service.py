from neo4j import Session

from src.kg.services.base_data_service import DataService
from src.db.db_schema import Readiness


class ReadinessService(DataService):

    def __init__(self, session: Session) -> None:

        super().__init__(session, Readiness)
        self.node_label = "Readiness"
        self.properties = [
            "id",
            "name",
            "ref",
            "hasSids",
            "hasLdc",
            "isNap",
            "approvedDate",
            "financingUsd",
        ]
        self.relationships = {
            "activityTypeId": {
                "label": "ActivityId",
                "direction": "OUT",
                "relation": "HAS",
            },
            "deliveryPartnerId": {
                "label": "DeliveryPartner",
                "direction": "OUT",
                "relation": "DONE_BY",
            },
            "statusId": {
                "label": "Status",
                "direction": "OUT",
                "relation": "HAS",
            },
            "regionId": {
                "label": "Region",
                "direction": "OUT",
                "relation": "HAS",
            },
        }
        # Configuration for the service node
        self.config = {
            "node_label": self.node_label,
            "properties": self.properties,
            "relationships": self.relationships,
        }

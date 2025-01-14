from neo4j import Session

from src.kg.services.base_data_service import DataService
from src.db.db_schema import Entity


class EntityService(DataService):

    def __init__(self, session: Session) -> None:

        super().__init__(session, Entity)
        self.node_label = "Entity"
        self.properties = ["id", "name", "code", "isDae"]
        self.relationships = {
            "countryId": {
                "label": "Country",
                "direction": "OUT",
                "relation": "IS_IN",
            },
            "entityTypeId": {
                "label": "EntityType",
                "direction": "OUT",
                "relation": "HAS",
            },
            "stageId": {
                "label": "Stage",
                "direction": "OUT",
                "relation": "HAS",
            },
            "sizeId": {
                "label": "Size",
                "direction": "OUT",
                "relation": "HAS",
            },
            "sectorId": {
                "label": "Sector",
                "direction": "OUT",
                "relation": "HAS",
            },
            "bmId": {
                "label": "Bm",
                "direction": "IN",
                "relation": "COVERS",
            },
            "projectId": {
                "label": "Project",
                "direction": "OUT",
                "relation": "FUNDS",
            },
        }
        # Configuration for the service node
        self.config = {
            "node_label": self.node_label,
            "properties": self.properties,
            "relationships": self.relationships,
        }

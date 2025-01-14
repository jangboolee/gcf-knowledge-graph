from neo4j import Session

from src.kg.services.base_data_service import DataService
from src.db.db_schema import Project


class ProjectService(DataService):

    def __init__(self, session: Session) -> None:

        super().__init__(session, Project)
        self.node_label = "Project"
        self.properties = ["id", "name", "ref", "financingUsd"]
        self.relationships = {
            "modalityId": {
                "label": "Modality",
                "direction": "OUT",
                "relation": "HAS",
            },
            "entityId": {
                "label": "Entity",
                "direction": "IN",
                "relation": "FUNDS",
            },
            "bmId": {
                "label": "BM",
                "direction": "IN",
                "relation": "COVERS",
            },
            "sectorId": {
                "label": "Sector",
                "direction": "OUT",
                "relation": "HAS",
            },
            "themeId": {
                "label": "Theme",
                "direction": "OUT",
                "relation": "HAS",
            },
            "sizeId": {
                "label": "Size",
                "direction": "OUT",
                "relation": "HAS",
            },
            "essCategoryId": {
                "label": "EssCategory",
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

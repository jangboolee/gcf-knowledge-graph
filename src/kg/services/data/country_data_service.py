from neo4j import Session

from src.kg.services.base_data_service import DataService
from src.db.db_schema import Country


class CountryDataService(DataService):

    def __init__(self, session: Session) -> None:

        super().__init__(session, Country)
        self.node_label = "Country"
        self.properties = None
        self.relationships = {
            "regionId": {
                "label": "Region",
                "direction": "OUT",
                "relation": "IS_IN",
            },
        }
        # Configuration for the service node
        self.config = {
            "node_label": self.node_label,
            "properties": self.properties,
            "relationships": self.relationships,
        }

    def _connect_to_regions(self) -> bool:
        """Custom helper method to connect Country nodes to Region nodes, as
        Country node metadata was already populated with country metadata nodes

        Returns:
            bool: True if successful, False if not
        """

        to_write = [
            {"countryId": i["id"], "regionId": i["regionId"]}
            for i in self.processed
        ]

        query = """
        UNWIND $data as record
        MATCH (c: Country {id: record.countryId})
        MATCH (r: Region {id: record.regionId})
        MERGE (c)-[:IS_IN]->(r)
        """

        return self.query_executor.execute_write(query, to_write)

    def populate(self) -> bool:
        """Overriden method for Country data service nodes that only populates
        the :IS_IN relationship with Region nodes

        Returns:
            bool: True after completion
        """

        self._get_data()
        self._process_data()
        self._connect_to_regions()

        return True

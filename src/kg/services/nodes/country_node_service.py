from src.kg.services.nodes.base_node_service import NodeService
from src.db.db_schema import CountryDict, Country

from neo4j import Session
import pandas as pd


class CountryService(NodeService):

    def __init__(self, session: Session) -> None:

        super().__init__(session, CountryDict)
        self.node_label = "Country"
        self.country_export_df = None

    def _read_country_export(self) -> bool:
        """Helper method to read in the country export file, required to map
        where a Country node is a SID (Small Island Developing State) or a
        LDC (Least Developed Country)

        Returns:
            bool: True after completion
        """

        with self.db_handler.get_session() as session:
            data = session.query(*Country.__table__.columns).all()
            columns = [col.name for col in Country.__table__.columns]

        self.country_export_df = pd.DataFrame(data, columns=columns)

        return True

    def _process_data(self) -> bool:
        """Overriden helper method to map SIDS and LDC boolean columns to the
        country data dictionary and format the dataframe to meet Neo4j styling
        requirements

        Returns:
            bool: True after completion
        """

        # Map SIDS and LDC boolean columns to country dictionary
        df = self.raw_df.merge(
            self.country_export_df[["iso3", "is_sids", "is_ldc"]],
            how="left",
            on="iso3",
        )

        # Assume countries not found in country export file are not SIDS or LDC
        cols = ["is_sids", "is_ldc"]
        for col in cols:
            df[col] = df[col].fillna(False).astype(bool)

        # Rename dataframe columns to align with property key camelcasing
        df.columns = [
            "id",
            "name",
            "iso2",
            "iso3",
            "code",
            "isSids",
            "isLdc",
        ]

        self.processed = df.to_dict(orient="records")

        return True

    def populate(self) -> bool:
        """Overriden main method with the additional calling of the custom
        and overriden helper methods

        Returns:
            bool: True if successful, False if not
        """

        # Retrieve and process data
        self._get_data()
        self._read_country_export()
        self._process_data()

        # Create Cypher query to populate the knowledge graph with the node
        query = f"""
        UNWIND $data as record
        MERGE (node: {self.node_label} {{id: record.id}})
        ON CREATE SET
            node += record
        """

        print(
            f"Populating graph with {len(self.processed)} "
            f"{self.node_label} nodes..."
        )

        return self.query_executor.execute_write(query, self.processed)

from typing import Type

from pandas import DataFrame
from neo4j import Session
from sqlalchemy.ext.declarative import DeclarativeMeta

from src.db.db_handler import DBHandler
from src.kg.db.query_executor import QueryExecutor


class MetaService:

    def __init__(
        self, session: Session, table_class: Type[DeclarativeMeta]
    ) -> None:

        self.session = session
        self.db_handler = DBHandler()
        self.query_executor = QueryExecutor(session)
        self.table_class = table_class
        # Instance variables to store node metadata
        self.node_label = None
        self.custom_keys = None
        # Instance variables to store data
        self.raw_df = None
        self.processed = None

    def _get_data(self) -> bool:
        """Helper method to retrieve the contents of the tabular DB table
        as a Pandas dataframe

        Returns:
            bool: True after completion
        """

        with self.db_handler.get_session() as session:
            data = session.query(*self.table_class.__table__.columns).all()
            columns = [col.name for col in self.table_class.__table__.columns]

        self.raw_df = DataFrame(data, columns=columns)

        return True

    def _process_data(self) -> bool:
        """Helper to process the raw DataFrame into a list of dictionaries

        Returns:
            bool: True if successful
        """

        # If custom keys are provided for the node
        if self.custom_keys:
            # Check if the custom keys are valid
            if len(self.custom_keys) != len(self.raw_df.columns):
                raise ValueError("Length of custom_keys do not match.")
            # Create a list of dictionaries with custom keys
            self.processed = [
                dict(zip(self.custom_keys, row))
                for row in self.raw_df.itertuples(index=False, name=None)
            ]
        else:
            # Use default column names as keys
            self.processed = self.raw_df.to_dict(orient="records")

        return True

    def populate(self) -> bool:
        """Main high-level method to populate the graph with the nodes

        Returns:
            bool: True if successful, False if not
        """

        # Retrieve and process data
        self._get_data()
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

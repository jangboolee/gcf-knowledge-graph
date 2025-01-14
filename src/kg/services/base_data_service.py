from typing import Type

from pandas import DataFrame
from neo4j import Session
from sqlalchemy.ext.declarative import DeclarativeMeta
from tqdm import tqdm

from src.db.db_handler import DBHandler
from src.kg.db.query_executor import QueryExecutor


class DataService:

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
        self.properties = None
        self.relationships = None
        self.config = None
        # Instance variables to store data
        self.raw_df = None
        self.processed = None

    @staticmethod
    def _snake_to_camel(snake_str: str) -> str:
        """Static helper method to convert snake_case column names into
        camelCase to adhere to Neo4j property styling conventions

        Args:
            snake_str (str): String in snake_case

        Returns:
            str: String converted to camelCase
        """

        parts = snake_str.split("_")
        return parts[0] + "".join(part.capitalize() for part in parts[1:])

    def _get_data(self) -> bool:
        """Helper method to retrieve the contents of the tabular DB table
        as a Pandas dataframe

        Returns:
            bool: True after completion
        """

        with self.db_handler.get_session() as session:
            data = session.query(*self.table_class.__table__.columns).all()
            cols = [col.name for col in self.table_class.__table__.columns]
            camel_cols = [self._snake_to_camel(col) for col in cols]

        self.raw_df = DataFrame(data, columns=camel_cols)

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

    def _create_and_connect(self, row: dict) -> bool:
        """Helper method to create and connect each data node

        Args:
            row (dict): Dictionary representation of a single row of the data
                table

        Returns:
            bool: True after completion
        """

        # Validate and retrieve node label and properties
        node_label = self.config["node_label"]
        properties = {
            key: row[key] for key in self.config["properties"] if key in row
        }

        # Create the main node
        create_query = f"""
        UNWIND $rows as row
        MERGE (n:{node_label} {{id: $id}})
        ON CREATE SET n += $properties
        RETURN n
        """
        self.session.run(create_query, id=row["id"], properties=properties)

        # Connect the main node with metadata nodes
        for key, rel_config in self.config["relationships"].items():
            if key in row and row[key] is not None:
                # Retrieve the node label to connect to and relationship data
                other_node_label = rel_config["label"]
                direction = rel_config["direction"]
                relation = rel_config["relation"]
                # Generate query based on direction
                if direction == "OUT":
                    rel_query = f"""
                    MATCH (n:{node_label} {{id: $node_id}})
                    MATCH (other:{other_node_label} {{id: $other_id}})
                    MERGE (n)-[:{relation}]->(other)
                    """
                else:
                    rel_query = f"""
                    MATCH (n:{node_label} {{id: $node_id}})
                    MATCH (other:{other_node_label} {{id: $other_id}})
                    MERGE (n)<-[:{relation}]-(other)
                    """
                self.session.run(
                    rel_query, node_id=row["id"], other_id=row[key]
                )

        return True

    def populate(self) -> bool:
        """Main high-level method to populate the graph with the nodes

        Returns:
            bool: True if successful, False if not
        """

        # Retrieve and process data
        self._get_data()
        self._process_data()

        # Create and connect each data node
        for row in tqdm(self.processed):
            self._create_and_connect(row)

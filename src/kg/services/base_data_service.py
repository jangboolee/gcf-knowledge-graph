from typing import Type

from pandas import DataFrame
from neo4j import Session
from sqlalchemy.ext.declarative import DeclarativeMeta
from tqdm import tqdm

from src.db.db_handler import DBHandler
from src.kg.db.query_executor import QueryExecutor


class DataService:

    def __init__(
        self,
        session: Session,
        table_class: Type[DeclarativeMeta],
        join_class: Type[DeclarativeMeta] = None,
    ) -> None:

        self.session = session
        self.db_handler = DBHandler()
        self.query_executor = QueryExecutor(session)
        self.table_class = table_class
        self.join_class = join_class
        # Instance variables to store node metadata
        self.node_label = None
        self.custom_keys = None
        self.properties = None
        self.relationships = None
        self.config = None
        # Instance variables to store data
        self.raw_df = None
        self.join_df = None
        self.processed = None
        self.join_processed = None

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

    def _get_data(self, for_join: bool = False) -> bool:
        """Helper method to retrieve the contents of the tabular DB table
        as a Pandas dataframe

        Args:
            for_join (bool, optional): Toggle to read optional join class.
                Defaults to False.

        Returns:
            bool: True after completion
        """

        with self.db_handler.get_session() as session:

            if for_join:
                data = session.query(*self.join_class.__table__.columns).all()
                cols = [col.name for col in self.join_class.__table__.columns]
            else:
                data = session.query(*self.table_class.__table__.columns).all()
                cols = [col.name for col in self.table_class.__table__.columns]
            camel_cols = [self._snake_to_camel(col) for col in cols]

        if for_join:
            self.join_df = DataFrame(data, columns=camel_cols)
        else:
            self.raw_df = DataFrame(data, columns=camel_cols)

        return True

    def _process_data(self, for_join: bool = False) -> bool:
        """Helper to process the raw DataFrame into a list of dictionaries

        Returns:
            bool: True if successful
        """

        if for_join:
            df = self.join_df
        else:
            df = self.raw_df

        # If custom keys are provided for the node
        if self.custom_keys:
            # Check if the custom keys are valid
            if len(self.custom_keys) != len(df.columns):
                raise ValueError("Length of custom_keys do not match.")
            # Create a list of dictionaries with custom keys
            processed = [
                dict(zip(self.custom_keys, row))
                for row in df.itertuples(index=False, name=None)
            ]
        else:
            # Use default column names as keys
            processed = df.to_dict(orient="records")

        if for_join:
            self.join_processed = processed
        else:
            self.processed = processed

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

    def _connect_join_countries(self) -> bool:
        """Helper method to use the join country tables to connect the data
        node to Country nodes

        Returns:
            bool: True if successful, False if not
        """

        # Get and process join country table for the data service
        self._get_data(for_join=True)
        self._process_data(for_join=True)

        # Generate ID key for the data service
        self_id_key = f"{self.node_label.lower()}Id"

        query = f"""
        UNWIND $data as record
        MATCH (r: {self.node_label} {{id: record.{self_id_key}}})
        MATCH (c: Country {{id: record.countryId}})
        MERGE (r)-[:GIVEN_TO]->(c)
        """

        return self.query_executor.execute_write(query, self.join_processed)

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

        # Connect countries for data node classes with join country data
        if self.join_class:
            self._connect_join_countries()

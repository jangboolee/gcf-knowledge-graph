import os
import logging

from neo4j import GraphDatabase
from neo4j.exceptions import (
    ServiceUnavailable,
    DriverError,
    ClientError,
    Neo4jError,
)


class Connection:

    def __init__(self) -> None:

        # Environment variables for graph connection
        self.kg_uri = os.environ.get("URI")
        self.user = os.environ.get("USERNAME")
        self.password = os.environ.get("PASSWORD")

        # Python driver to connect to graph database
        self.driver = None

    def connect(self) -> bool:
        """Method to establish a Python driver connection to the Neo4j graph DB

        Returns:
            bool: True if connected, False if not
        """

        try:
            self.driver = GraphDatabase.driver(
                self.kg_uri, auth=(self.user, self.password)
            )
            logging.info("Connected to graph DB.")
            return True
        except (ServiceUnavailable, DriverError, ClientError, Neo4jError) as e:
            logging.error(f"Failed to connect to graph DB: {e}")
            return False

    def close(self) -> bool:
        """Method to close the Python driver connection

        Returns:
            bool: True if closed, False if not
        """

        if self.driver:
            self.driver.close()
            logging.info("Closed connection to graph DB")
            return True
        else:
            logging.warning("No active graph DB connection to close")
            return False

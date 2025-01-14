import logging

from src.kg.db.connection import Connection
from src.kg.db.query_executor import QueryExecutor
from src.kg import (
    ActivityTypeService,
    CountryService,
    DeliveryPartnerService,
    EntityTypeService,
    EssCategoryService,
    ModalityService,
    RegionService,
)


class KnowledgeGraph:

    def __init__(self, conn: Connection) -> None:

        # Connect to the database and open an active session
        self.database = "neo4j"
        self.conn = conn
        self.session = None
        self._open_session()
        # Instantiate query executor interface
        self.query_executor = QueryExecutor(self.session)

    def _open_session(self) -> bool:
        """Helper method to open a session using the Connection class

        Raises:
            RuntimeError: Raises error if Connection.connect() has not been
                previously called

        Returns:
            bool: True if successfully opened, False if not
        """

        if not self.conn.driver:
            raise RuntimeError("Connection not established")
        else:
            self.session = self.conn.driver.session(database=self.database)
            logging.info("Session opened successfully")
            return True

    def _close_session(self) -> bool:
        """Helper method to close the active session

        Returns:
            bool: True if session is successfully closed, False if not
        """

        if self.session:
            self.session.close()
            logging.info("Session closed successfully")
            return True
        else:
            logging.warning("No active session to close.")
            return False

    def close(self) -> bool:
        """Close the session and driver connection to the graph DB

        Returns:
            bool: True after successful completion, False if any errors
        """

        return all([self._close_session(), self.conn.close()])

    def initialize(self) -> bool:

        # Initialize node services for populating nodes
        services = [
            ActivityTypeService(self.session),
            RegionService(self.session),
            CountryService(self.session),
            DeliveryPartnerService(self.session),
            EntityTypeService(self.session),
            EssCategoryService(self.session),
            ModalityService(self.session),
        ]

        # Initialize and populate each service
        for service in services:
            service.populate()


if __name__ == "__main__":

    conn = Connection()
    conn.connect()

    kg = KnowledgeGraph(conn=conn)
    kg.initialize()

    kg.close()

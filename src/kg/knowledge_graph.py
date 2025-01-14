import logging

from src.db.db_handler import DBHandler
from src.kg.db.connection import Connection
from src.kg.db.query_executor import QueryExecutor
from src.kg import (
    ActivityTypeService,
    BmNodeService,
    CountryService,
    DeliveryPartnerService,
    EntityTypeService,
    EssCategoryService,
    ModalityService,
    RegionService,
    SectorService,
    SizeService,
    StageService,
    StatusService,
    ThemeService,
    ProjectService,
)


class KnowledgeGraph:

    def __init__(self, conn: Connection) -> None:

        # Instantiate singleton DB Handler to read from tabular DB
        self.db_handler = DBHandler()
        # Connect to the database and open an active session
        self.database = "neo4j"
        self.conn = conn
        self.session = None
        self._open_session()
        # Instantiate singleton query executor interface
        self.query_executor = QueryExecutor(self.session)
        # Service classes for each metadata node type
        self.meta_services = {
            "activity_type": ActivityTypeService(self.session),
            "bm": BmNodeService(self.session),
            "country": CountryService(self.session),
            "delivery_partner": DeliveryPartnerService(self.session),
            "entity_type": EntityTypeService(self.session),
            "ess_category": EssCategoryService(self.session),
            "modality": ModalityService(self.session),
            "region": RegionService(self.session),
            "sector": SectorService(self.session),
            "size": SizeService(self.session),
            "stage": StageService(self.session),
            "status": StatusService(self.session),
            "theme": ThemeService(self.session),
        }
        self.data_services = {"project": ProjectService(self.session)}

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
        """Main method to initialize the GCF Knowledge Graph with all
        metadata nodes

        Returns:
            bool: True after completion
        """

        # Initialize and populate each service
        for service in self.meta_services.values():
            service.populate()

        return True

    def populate(self) -> bool:

        for service in self.data_services.values():
            service.populate()


if __name__ == "__main__":

    conn = Connection()
    conn.connect()

    kg = KnowledgeGraph(conn=conn)
    # kg.initialize()
    kg.populate()

    kg.close()

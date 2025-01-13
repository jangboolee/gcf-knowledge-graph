from src.kg.db.connection import Connection


class KnowledgeGraph:

    def __init__(self, conn: Connection) -> None:

        # Connect to the database and open an active session
        self.database = "neo4j"
        self.conn = conn
        self.session = None
        self.query_executor = None

    def _open_session(self) -> bool:
        pass

    def _close_session(self) -> bool:
        pass

    def close(self) -> bool:
        pass


if __name__ == "__main__":

    conn = Connection()
    conn.connect()

    kg = KnowledgeGraph(conn=conn)
    kg.close()

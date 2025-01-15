from src.kg.db.connection import Connection
from src.kg.knowledge_graph import KnowledgeGraph


def main():

    conn = Connection()
    conn.connect()

    kg = KnowledgeGraph(conn=conn)

    # Initialize graph with metadata nodes
    kg.initialize()
    # Populate graph with data nodes
    kg.populate()

    kg.close()


if __name__ == "__main__":

    main()

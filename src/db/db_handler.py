from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, configure_mappers

from src.db.db_schema import Base


class DBHandler:

    def __init__(self, db_uri: str = "sqlite:///data/gcf_data.db") -> None:

        self.db_uri = db_uri
        self.engine = create_engine(self.db_uri, echo=True)
        self.Session = sessionmaker(bind=self.engine)

    def create_all(self) -> bool:

        Base.metadata.create_all(self.engine)
        configure_mappers()
        return True

    def drop_all(self) -> bool:

        Base.metadata.drop_all(self.engine)
        return True

    def get_session(self) -> Session:
        return self.Session()


if __name__ == "__main__":

    handler = DBHandler()
    handler.create_all()

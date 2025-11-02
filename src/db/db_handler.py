from sqlalchemy import create_engine
from sqlalchemy.orm import Session, configure_mappers, sessionmaker

from src.db.db_schema import Base
from src.utils.singleton import Singleton


class DBHandler(Singleton):
    def __init__(self, db_uri: str = "sqlite:///data/gcf_data.db") -> None:
        # Avoid reinitializing in singleton
        if not hasattr(self, "initialized"):
            self.initialized = True
        self.db_uri = db_uri
        self.engine = create_engine(self.db_uri, echo=False)
        self.Session = sessionmaker(bind=self.engine)
        # Ensure all tables exist when DB Handler is instantiated
        self.create_all()

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

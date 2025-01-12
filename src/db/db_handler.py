from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, session

from src.db.db_schema import Base


class DbHandler:

    def __init__(self, db_uri: str = "sqlite:///data/gcf_data.db") -> None:

        self.db_uri = db_uri
        self.engine = create_engine(self.db_uri, echo=True)
        self.Session = sessionmaker(bind=self.engine)

    def create_all(self) -> bool:

        Base.metadata.create_all(self.engine)
        return True

    def drop_all(self) -> bool:

        Base.metadata.drop_all(self.engine)
        return True


if __name__ == "__main__":

    handler = DbHandler()
    handler.create_all()

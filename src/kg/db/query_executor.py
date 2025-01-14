import logging
from typing import Union

from neo4j import Session
from neo4j.exceptions import (
    ServiceUnavailable,
    DriverError,
    ClientError,
    Neo4jError,
)
from pandas import DataFrame
from tqdm import tqdm

from src.utils.singleton import Singleton


class QueryExecutor(Singleton):

    def __init__(self, session: Session) -> None:

        # Avoid reinitializing in singleton
        if not hasattr(self, "initialized"):
            self.initialized = True
        self.session = session

    @staticmethod
    def _chunk_list(data: list, chunk_size: int = 500) -> list:
        """Helper static method to chunk a large list into sublists of chunks

        Args:
            data (list): List of data to chunk
            chunk_size (int, optional): Size per chunk. Defaults to 500.

        Yields:
            Iterator[list]: Sublists of chunks
        """

        for i in range(0, len(data), chunk_size):
            yield data[i : i + chunk_size]

    def execute_read(
        self, query: str, params: dict = None, return_df: bool = False
    ) -> Union[list[dict], DataFrame]:
        """Execute a read/MATCH query

        Args:
            query (str): Cyper query for reading
            params (dict, optional): Additional parameters to use for the
                Cypher query. Defaults to None.
            return_df (bool, optional): Toggle to return the results as a
                pandas dataframe and not as a list of dictionaries.
                Defaults to False.

        Returns:
            Union[list[dict], DataFrame]: Results of the Cypher query
        """

        try:
            with self.session.begin_transaction() as tx:

                # Get the results of the Cypher query
                result = tx.run(query, params or {})
                # Convert the results as a list of dictionaries
                records = [record.data() for record in result]

                if return_df:
                    return DataFrame(records)
                else:
                    return records

        except (ServiceUnavailable, DriverError, ClientError, Neo4jError) as e:
            logging.error(f"{query} raised an error: \n{e}")
            raise

    def execute_write(
        self, query: str, data: list[dict], chunk_size: int = 500
    ) -> bool:
        """Method to chunk up a list of dictionaries prepared for Cypher
        parameterization and call `execute_write()` for each chunk

        Args:
            query (str): Cypher query to execute
            data (list[dict]): List of dictionaries for Cypher parameterization
            chunk_size (int, optional): Number of records per batch.
                Defaults to 500.

        Returns:
            bool: True if successful, False if not
        """

        try:
            with tqdm(total=len(data)) as pbar:
                for chunk in self._chunk_list(data, chunk_size):
                    self.session.execute_write(
                        lambda tx: tx.run(query, data=chunk)
                    )
                    pbar.update(len(chunk))
                return True
        except (ServiceUnavailable, DriverError, ClientError, Neo4jError) as e:
            logging.error(f"{query} raised an error: \n{e}")
            raise
        return False

import logging
import traceback
import psycopg2

logging.basicConfig(level=logging.INFO)

class Database:
    """
    A class representing a database connection.

    Attributes:
        _user (str): The username for the database connection.
        _password (str): The password for the database connection.
        _host (str): The host address for the database connection.
        _port (str): The port number for the database connection.
        _dbname (str): The name of the database.
        _connection (psycopg2.extensions.connection): The database connection object.
        _cursor (psycopg2.extensions.cursor): The database cursor object.

    Methods:
        connect: Connects to the database.
        disconnect: Disconnects from the database.
    """

    def __init__(self):
        logging.info("Initializing database connection")
        self._connection = None
        self._cursor = None

    async def db_connect(self):
        """
        Connects to the database.

        Raises:
            psycopg2.Error: If there is an error connecting to the database.
        """
        try:
            self._connection = psycopg2.connect('postgres://avnadmin:AVNS_S5y9umxi3E1z1gETw3f@emcomplain-queries-ysamyakjain.a.aivencloud.com:16176/defaultdb?sslmode=require')
            self._cursor = self._connection.cursor()
            logging.info("Connected to database")
        except psycopg2.Error as e:
            logging.error("Error connecting to database")
            logging.error(traceback.format_exc())
            raise e
        
    async def db_execute_query(self, query, params=None):
        """
        Executes a query on the database.

        Args:
            query (str): The query to execute.
            params (tuple, optional): The parameters to use with the query. Defaults to None.

        Returns:
            list: The results of the query.
        """
        try:
            if params:
                self._cursor.execute(query, params)
            else:
                self._cursor.execute(query)
            self._connection.commit()
            logging.info("Executed query")
        except psycopg2.Error as e:
            logging.error("Error executing query")
            logging.error(traceback.format_exc())
            raise e

    async def db_fetch_results(self, query, params=None):
        """
        Fetches the results of a query.

        Returns:
            list: The results of the query.
        """
        try:
            if params:
                self._cursor.execute(query, params)
            else:
                self._cursor.execute(query)

            results = self._cursor.fetchall()
            logging.info("Fetched results")
            return results
        except psycopg2.Error as e:
            logging.error("Error fetching results")
            logging.error(traceback.format_exc())
            raise e
    
    async def db_disconnect(self):
        """
        Disconnects from the database.

        Raises:
            psycopg2.Error: If there is an error disconnecting from the database.
        """
        try:
            if self._cursor:
                self._cursor.close()
            if self._connection:
                self._connection.close()
            logging.info("Disconnected from database")
        except psycopg2.Error as e:
            logging.error("Error disconnecting from database")
            logging.error(traceback.format_exc())
            raise e

import duckdb


class BaseConnection:
    """
    Base class for database connections.
    """
    def connect(self):
        """
        Connect to the database.
        """
        


class DDBConnection(BaseConnection):
    """
    A connection object for DuckDB.
    """
    def connect(self):
        """
        Connect to the DuckDB database.

        Returns:
            duckdb.Connection: A connection object for the DuckDB database.
        """
        
        return duckdb.connect("motherduck:")
    
    def attach(self, db_path: str):
        """
        Attach a database to the DuckDB database.

        Args:
            db_path (str): The path to the database to attach.

        Returns:
            duckdb.Cursor: A cursor object for the DuckDB database.
        """
        return self.connect().sql(f"ATTACH DATABASE '{db_path}' AS diffstore")


def get_connection(db_type: str):
    """
    Get a connection object for the database type.

    Args:
        db_type (str): The type of database to connect to.

    Returns:
        BaseConnection: A connection object for the database type.
    """
    if db_type == "duckdb":
        return DDBConnection()
    else:
        raise ValueError(f"Unknown database type '{db_type}'")
    

# conn = get_connection("duckdb")
# conn.connect()
# attach a .duckdb file to motherduck
# conn.attach("mydb.duckdb")




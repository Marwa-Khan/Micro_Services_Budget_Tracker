from psycopg2 import pool

# Configuration for account_service database
ACCOUNT_SERVICE_CONFIG = {
    'dbname': 'account_service',
    'user': 'postgres',
    'password': '9009',
    'host': 'localhost',
    'port': '5432'
}

# Configuration for expense_service database
EXPENSE_SERVICE_CONFIG = {
    'dbname': 'expense_service',
    'user': 'postgres',
    'password': '9009',
    'host': 'localhost',
    'port': '5432'
}

# Connection pools
account_connection_pool = pool.SimpleConnectionPool(
    1, 20,
    dbname=ACCOUNT_SERVICE_CONFIG['dbname'],
    user=ACCOUNT_SERVICE_CONFIG['user'],
    password=ACCOUNT_SERVICE_CONFIG['password'],
    host=ACCOUNT_SERVICE_CONFIG['host'],
    port=ACCOUNT_SERVICE_CONFIG['port']
)

expense_connection_pool = pool.SimpleConnectionPool(
    1, 20,
    dbname=EXPENSE_SERVICE_CONFIG['dbname'],
    user=EXPENSE_SERVICE_CONFIG['user'],
    password=EXPENSE_SERVICE_CONFIG['password'],
    host=EXPENSE_SERVICE_CONFIG['host'],
    port=EXPENSE_SERVICE_CONFIG['port']
)

def get_account_db_connection():
    """Retrieve a connection from the account_service pool."""
    if account_connection_pool:
        return account_connection_pool.getconn()

def release_account_db_connection(conn):
    """Release a connection back to the account_service pool."""
    if account_connection_pool:
        account_connection_pool.putconn(conn)

def get_expense_db_connection():
    """Retrieve a connection from the expense_service pool."""
    if expense_connection_pool:
        return expense_connection_pool.getconn()

def release_expense_db_connection(conn):
    """Release a connection back to the expense_service pool."""
    if expense_connection_pool:
        expense_connection_pool.putconn(conn)

import paramiko
import mysql.connector
from sshtunnel import SSHTunnelForwarder
import logging
import MySQLdb

def connect_via_ssh_with_private_key_and_query():
    ssh_host = '34.170.255.102'
    ssh_port = 22  # Default SSH port
    ssh_username = 'mamoudou_sow'
    private_key_path = 'C:\\Users\\MamoudouMamadouSOW\\Documents\\Scripts\\Python\\Reconciliation Scripts\\cle_open_ssh'  # Private key file path

    # Remote MySQL server details
    remote_mysql_host = '127.0.0.1'  # MySQL is running on the remote server
    remote_mysql_port = 3306  # Default MySQL port
    remote_mysql_user = 'mamoudou_sow'
    remote_mysql_password = 'BpCXq6C6Kyl6E5gIIXvj'
    remote_mysql_db = 'GU_GLOBAL'

    # Add logging to troubleshoot
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger()

    # Use the private key for SSH authentication
    private_key = paramiko.RSAKey.from_private_key_file(private_key_path)

    # Open SSH tunnel using the private key
    with SSHTunnelForwarder(
        (ssh_host, ssh_port),
        ssh_username=ssh_username,
        ssh_pkey=private_key,  # Using private key instead of password
        remote_bind_address=(remote_mysql_host, remote_mysql_port),
        local_bind_address=('127.0.0.1', 3307),  # Local port forwarding
        logger=logger
    ) as tunnel:
        
        # Connect to the MySQL database via the SSH tunnel
        try:
            # Establish the MySQL connection
            print("Establish the MySQL connection")
            connection = MySQLdb.connect(
                host='127.0.0.1',  # Connecting to localhost via the SSH tunnel
                port=3307,  # The forwarded port from the SSH tunnel
                user=remote_mysql_user,  # MySQL username
                passwd=remote_mysql_password,  # MySQL password
                db=remote_mysql_db  # Database name
            )

            cursor = connection.cursor()

            # Test query to check connection
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()
            print(f"Connected to database: {db_name[0]}")

            # You can now execute queries here
            # For example: cursor.execute("SELECT * FROM your_table;")

        except MySQLdb.Error as e:
            print(f"Error connecting to MySQL: {e}")

        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    connect_via_ssh_with_private_key_and_query()

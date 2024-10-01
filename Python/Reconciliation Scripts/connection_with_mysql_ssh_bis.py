import signal
import sys
import paramiko
import MySQLdb
from sshtunnel import SSHTunnelForwarder
import time 
from datetime import datetime, timedelta

# Global connection and cursor variables
connection = None
cursor = None
tunnel = None

def fetch_transactions_for_period(connection, start, end):
    cursor = connection.cursor()

    # Start and end date for the query (adjust according to your needs)
    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")

    # Open the file to write results
    current_date = start_date
    
    # Loop through each day in the date range
    while current_date <= end_date:
        jour = current_date.strftime("%Y-%m-%d")
        file_name = f"tuple_gu1_{jour}.txt"  # Generate the file name for each day

        # SQL query for the day
        query = f"""
            SELECT num_transaction_gu FROM transactiongu
            WHERE statut_code = 'TRANSACTION_NORMALE' and salepoint_code in (
            'SNCHT23858','GUUCI10863', 'GUUCM9030', 'GUUGN4686', 'GUUML6541', 'GUUBF2938', 'GUUML6541')
            AND transaction_date BETWEEN '{jour} 00:00:00' AND '{jour} 23:59:59';
        """
        
        cursor.execute(query)
        results = cursor.fetchall()

        # Store the results in a list of tuples
        transactions_list = [row[0] for row in results]

        # Print the size of the list for the current day
        print(f"Date: {jour}, Number of transactions: {len(transactions_list)}")

        # Write the list of tuples to a new file for each day
        with open(file_name, "w") as f:
            f.write(str(tuple(transactions_list))) 
        
        # Move to the next day
        current_date += timedelta(days=1)


    # Clean up
    cursor.close()
    connection.close()
    print("Transaction retrieval completed.")

def signal_handler(sig, frame):
    """Handle the exit signal (Ctrl+C) and clean up resources."""
    print("\nReceived Ctrl+C. Exiting and cleaning up...")
    
    # Ensure the MySQL cursor and connection are closed
    if cursor:
        cursor.close()
    if connection:
        connection.close()
        print("MySQL connection closed.")

    # Stop the SSH tunnel manually
    if tunnel and tunnel.is_active:
        print("Stopping SSH tunnel...")
        tunnel.stop()
        print("SSH tunnel stopped.")
    
    # Exit the program
    sys.exit(0)

def connect_via_ssh_with_private_key_and_query(start, end):
    global connection, cursor, tunnel

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

    # Use the private key for SSH authentication
    private_key = paramiko.RSAKey.from_private_key_file(private_key_path)

    # Initialize the SSH tunnel
    tunnel = SSHTunnelForwarder(
        (ssh_host, ssh_port),
        ssh_username=ssh_username,
        ssh_pkey=private_key,  # Using private key instead of password
        remote_bind_address=(remote_mysql_host, remote_mysql_port),
        local_bind_address=('127.0.0.1', 3307)  # Local port forwarding
    )

    try:
        # Start the SSH tunnel manually
        print("Starting SSH tunnel...")
        tunnel.start()
        
        print("SSH tunnel started. Establishing the MySQL connection...")

        # Establish the MySQL connection via the tunnel
        connection = MySQLdb.connect(
            host='127.0.0.1',  # Connecting to localhost via the SSH tunnel
            port=3307,  # The forwarded port from the SSH tunnel
            user=remote_mysql_user,  # MySQL username
            passwd=remote_mysql_password,  # MySQL password
            db=remote_mysql_db  # Database name
        )

        fetch_transactions_for_period(connection=connection, start=start, end=end)

        print("MySQL connection is active. Press Ctrl+C to exit.")
        
        # Keep the program running, waiting for Ctrl+C to exit
        while True:
            time.sleep(1)  # Sleep for a second and keep looping (wait for Ctrl+C)


    except MySQLdb.Error as e:
        print(f"Error connecting to MySQL: {e}")

    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage: python script.py <start_date> <end_date>")
        sys.exit(1)

    start = sys.argv[1]
    end = sys.argv[2]

    if( start > end) :
        print("Usage: the first date must be lessier than ")
        sys.exit(1)

    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    if( datetime.strptime(end,"%Y-%m-%d") >= today) :
        print(" the end date " + end + " must be earliser than today " + str(today) + ".")
        sys.exit(1)
    
    # Register the signal handler for Ctrl+C (SIGINT)
    signal.signal(signal.SIGINT, signal_handler)

    # Start the SSH tunnel and MySQL connection
    connect_via_ssh_with_private_key_and_query(start=start, end=end)

"""
Database operations for ABC tunes
"""

from typing import List, Dict, Optional, Any
import mysql.connector
from mysql.connector import Error 


def connect_to_database() -> Optional[mysql.connector.connection.MySQLConnection]:
    """
    Establish connection to MySQL database.

    Returns:
            MySQL connection object or None if connection fails 
    """

    try:
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root',
            database = 'abc_tunes_db'
        )
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

def create_database_schema(conn: mysql.connector.connection.MySQLConnection) -> bool:
    """
    Create the tunes table if it doesnt exist

    Args:
        conn: MySQL connection object
    
    Returns:
            True if successful, False otherwise
    """
    try:
        cursor = conn.cursor()
    
        # Create tunes table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS tunes ( 
        id INT AUTO_INCREMENT PRIMARY KEY,
        book_number INT NOT NULL,
        reference_number VARCHAR(50),
        title VARCHAR(255),
        type VARCHAR(100),
        meter VARCHAR(50),
        key_signature VARCHAR(50),
        abc_notation TEXT,
        file_path VARCHAR(500),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """

        cursor.execute(create_table_query)
        conn.commit()
        cursor.close()

        print("Database schema created successfully")
        return True

    except Error as e:
        print(f"Error creating schema: {e}")
        return False

def insert_tune(conn: mysql.connector.connection.MySQLConnection, tune: Dict[str, str], book_number: int, file_path: str) -> bool:
    """
    Insert a single tune into the database

    Args: 
        conn: MySQL connection object 
        tune: Dictionary containing tune metadata
        book_number: Book/folder number
        file_path: Path to the source ABC file 

    Returns:
        True if successful, False otherwise
    """

    try:
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO tunes (book_number, reference_number, title, type, meter, key_signature, abc_notation, file_path)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            book_number,
            tune.get('reference_number', ''),
            tune.get('title', ''),
            tune.get('type', ''),
            tune.get('meter', ''),
            tune.get('key', ''),
            tune.get('abc_notation', ''),
            file_path
        )

        cursor.execute(insert_query, values)
        conn.commit()
        cursor.close()

        return True
    
    except Error as e:
        print(f"Error inserting tune: {e}")
        return False
    
def insert_tunes_batch(conn: mysql.connector.connection.MySQLConnection, tunes: List[Dict[str, str]], book_number: int, file_path: str) -> int:
    """
    Insert multiple tunes from one file into the database 

    Args: 
        conn: MySQL connection object
        tunes: List of tiune dictionaries
        file_path: path to tunes successfully inserted 

    Retruns:
        Number of tunes successfully inserted
    """

    count = 0 
    for tune in tunes:
        if insert_tune(conn, tune, book_number, file_path):
            count+= 1
    return count

# Update tune feature
def update_tune(conn: mysql.connector.connection.MySQLConnection,
                tune_id: int,
                updates: Dict[str, str]) -> bool:
    """
    Update a tunes information in the database.

    Args:
    conn: MySQL connection object
    tune_id: ID of the tune to update
    updates: Dictionary of field names and values

    Returns:
    True if successful False otherwise
    """

    try:
        cursor = conn.cursor()

        # Build and update the query
        set_clause = ",".join([f"{key} = %s" for key in updates.keys()])
        query = f"UPDATE tunes SET {set_clause} WHERE id = %s"

        #values for the query
        values = list(updates.values()) + [tune_id]

        cursor.execute(query, values)
        conn.commit()

        if cursor.rowcount > 0:
            cursor.close()
            return True
        else:
            print(f"No tune found with ID {tune_id}")
            cursor.close()
            return False
    except Error as e:
        print(f"Error updating tune: {e}")
        return False

# Delete tune feature    
def delete_tune(conn: mysql.connector.connection.MySQLConnection, 
                tune_id: int) -> bool:
    """
    Delete a tune from the database.

    Args:
    conn: MySQL connection object
    tune_id: ID of the tune thats being deleted

    Return:
    TRue if successful false if not
    """

    try:
        cursor = conn.cursor()

        query = "DELETE FROM tunes WHERE id = %s"
        cursor.execute(query, (tune_id,))
        conn.commit()

        if cursor.rowcount > 0:
            cursor.close()
            return True
        else:
            print(f"No tune found with ID: {tune_id}")
            cursor.close()
            return False
        
    except Error as e:
        print(f"Error deleting tune: {e}")
        return False
    
def get_tune_by_id(conn: mysql.connector.connection.MySQLConnection,
                   tune_id: int) -> Optional[Dict[str, Any]]:
    """
    Get a single tune by its ID.

    Args:
    conn: MySQL connection object
    tune_id: ID of the tune to retrieve

    returns: 
    dictionary with tune data or none if not found
    """

    try:
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM tunes WHERE id = %s"
        cursor.execute(query, (tune_id,))

        result = cursor.fetchone()
        cursor.close()

        return result
    
    except Error as e:
        print(f"Error retrieving tune: {e}")
        return None


# test the database function 
if __name__ == '__main__':
    print("testing database function")

    # test connection
    conn = connect_to_database()

    if conn:
        print("Connected to database successfully")

        # Create schema
        create_database_schema(conn)

        # Test insert with sample data
        sample_tune = {
            'reference_number': '1',
            'title': 'Test Tune',
            'type': 'reel',
            'meter': '4/4',
            'key': 'D',
            'abc_notation': 'X:1\nT:Test Tune\nK:D\n|:def|'
        }

        print("\nTesting tune insertion...")
        if insert_tune(conn, sample_tune, 0, 'test_abc'):
            print("Test tune inserted successfully!")

        # Check if it was inserted 
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM TUNES")
        count = cursor.fetchone()[0]
        print(f"\nTotal tunes in database {count}")
        cursor.close()

        conn.close()
    else:
        print("Failed to connect to database")

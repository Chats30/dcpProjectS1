"""
Main entry point for ABC Tune Database application
"""

from file_loader import find_abc_files
from abc_parser import parse_abc_file
from database import connect_to_database, create_database_schema, insert_tunes_batch


def load_all_tunes():
    """
    Load all tunes from files into database.

    This function:
    - Finds all abc files in the abc_books directory
    - Parses each file to extract tune metadata
    - Inserts all tunes into the MySQL database
    """
    print("=" * 60)
    print("ABC tunes dataset loader")
    print("="* 60)

    # Connect to database 
    print("\n[1/4] Connecting to database...")
    conn = connect_to_database()
    if not conn:
        print("Failed to connect to database. Exiting")
        return
    print("Connected to database successfully :)")

    # Creating table schema 
    print("\n[2/4] Creating database schema...")
    if not create_database_schema(conn):
        print("Failed to create schema. Exiting")
        conn.close()
        return
    print("Schema ready")

    # FInd all abc files
    print("\n[3/4] Finding ABC files...")
    abc_files = find_abc_files('abc_books')
    print(f"Found {len(abc_files)} ABC files")

    # parse and load each file 
    print("\n[4/4] Parsing and loading tunes...")
    total_tunes = 0
    files_processed = 0

    for book_number, file_path in abc_files:
        try:
            # parse the file 
            tunes = parse_abc_file(file_path)

            if tunes:

                # inserting tunes into database
                count = insert_tunes_batch(conn, tunes, book_number, file_path)
                total_tunes += count
                files_processed += 1

                print(f"{file_path}: {count} tunes")
            else:
                print(f"{file_path}: No tunes found")

        except Exception as e:
            print(f" {file_path}: Error - {e}")
    
    # close the datbase
    conn.close()

    # print summary
    print("\n" + "=" * 60)
    print("LOADING COMPLETE!")
    print(f"FIles processed: {files_processed}/{len(abc_files)}")
    print(f"Total tunes loaded: {total_tunes}")
    print("="*60)

def main():
    """Main function to run the application"""

    load_all_tunes()

if __name__ == "__main__":
    main()
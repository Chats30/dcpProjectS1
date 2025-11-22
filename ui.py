"""
User interface for ABC Tune database
"""

from analysis import (
    load_tunes_from_database,
    get_tunes_by_book,
    get_tunes_by_type,
    search_tunes,
    get_tunes_by_key,
    count_tunes_per_book,
    get_most_common_types,
    get_most_common_keys,
    get_summary_statistics
)

from tabulate import tabulate
import pandas as pd


def display_menu():
    """Display the main menu options"""
    print("\n" + "=" * 60)
    print("ABC TUNE DATABASE - MAIN MENU")
    print("=" * 60)
    print("1. View all tunes from a specific book")
    print("2. Search tunes by type")
    print("3. Search tunes by title")
    print("4. Search tunes by key signature")
    print("5. View statistics")
    print("6. View tunes per book")
    print("7. View most common tune types")
    print("8. View most common keys")
    print("9. Exit")
    print("=" * 60)

def display_dataframe(df: pd.DataFrame, max_rows: int = 10):
    """
    Displaying the dataframe in a table format

    args:
        df: DataFrame to display
        max_rows: Maximum nmber of rows to show
    """
    if df.empty:
        print("\n No results found")
        return
    
    # Select columns to display
    display_columns = ['id', 'book_number', 'title', 'type', 'key_signature', 'meter']
    df_display = df[display_columns]

    if len(df) > max_rows:
        print(f"\n Showing first {max_rows} of {len(df)} results:")
        df_display = df_display.head(max_rows)
    else:
        print(f"\n Found {len(df)} results:")
    
    print(tabulate(df_display, headers='keys', tablefmt='grid', showindex=False))
    
    if len(df) > max_rows:
        print(f"\n... and {len(df) - max_rows} more results")


def handle_view_by_book(df: pd.DataFrame):
    """Handle viewing tunes from a specific book."""
    print("\n" + "-" * 60)
    print("VIEW TUNES BY BOOK")
    print("-" * 60)
    
    # Show available books
    book_counts = count_tunes_per_book(df)
    print("\nAvailable books:")
    for book_num, count in book_counts.items():
        print(f"  Book {book_num}: {count} tunes")
    
    try:
        book_number = int(input("\nEnter book number: "))
        results = get_tunes_by_book(df, book_number)
        display_dataframe(results)
    except ValueError:
        print(" Invalid input. Please enter a number.")


def handle_search_by_type(df: pd.DataFrame):
    """Handle searching tunes by type."""
    print("\n" + "-" * 60)
    print("SEARCH BY TUNE TYPE")
    print("-" * 60)
    
    # Show common types
    print("\nMost common types:")
    top_types = get_most_common_types(df, 5)
    for tune_type, count in top_types.items():
        print(f"  {tune_type}: {count} tunes")
    
    tune_type = input("\nEnter tune type to search (e.g., reel, jig): ").strip()
    if tune_type:
        results = get_tunes_by_type(df, tune_type)
        display_dataframe(results)
    else:
        print(" Please enter a tune type.")


def handle_search_by_title(df: pd.DataFrame):
    """Handle searching tunes by title."""
    print("\n" + "-" * 60)
    print("SEARCH BY TITLE")
    print("-" * 60)
    
    search_term = input("\nEnter search term: ").strip()
    if search_term:
        results = search_tunes(df, search_term)
        display_dataframe(results)
    else:
        print(" Please enter a search term.")


def handle_search_by_key(df: pd.DataFrame):
    """Handle searching tunes by key signature."""
    print("\n" + "-" * 60)
    print("SEARCH BY KEY SIGNATURE")
    print("-" * 60)
    
    # Show common keys
    print("\nMost common keys:")
    top_keys = get_most_common_keys(df, 5)
    for key, count in top_keys.items():
        print(f"  {key}: {count} tunes")
    
    key_signature = input("\nEnter key signature (e.g., D, G, Am): ").strip()
    if key_signature:
        results = get_tunes_by_key(df, key_signature)
        display_dataframe(results)
    else:
        print("Please enter a key signature.")


def handle_view_statistics(df: pd.DataFrame):
    """Handle displaying summary statistics."""
    print("\n" + "-" * 60)
    print("SUMMARY STATISTICS")
    print("-" * 60)
    
    stats = get_summary_statistics(df)
    
    print(f"\n Total Tunes: {stats['total_tunes']}")
    print(f" Total Books: {stats['total_books']}")
    print(f" Total Tune Types: {stats['total_types']}")
    print(f" Total Key Signatures: {stats['total_keys']}")
    print(f" Most Common Type: {stats['most_common_type']}")
    print(f" Most Common Key: {stats['most_common_key']}")


def handle_view_tunes_per_book(df: pd.DataFrame):
    """Handle displaying tune counts per book."""
    print("\n" + "-" * 60)
    print("TUNES PER BOOK")
    print("-" * 60)
    
    counts = count_tunes_per_book(df)
    print()
    for book_num, count in counts.items():
        print(f" Book {book_num}: {count} tunes")


def handle_view_common_types(df: pd.DataFrame):
    """Handle displaying most common tune types."""
    print("\n" + "-" * 60)
    print("MOST COMMON TUNE TYPES")
    print("-" * 60)
    
    try:
        n = int(input("\nHow many top types to display? (default 10): ") or "10")
        top_types = get_most_common_types(df, n)
        
        print(f"\n Top {n} Tune Types:")
        for i, (tune_type, count) in enumerate(top_types.items(), 1):
            print(f"{i}. {tune_type}: {count} tunes")
    except ValueError:
        print(" Invalid input. Please enter a number.")


def handle_view_common_keys(df: pd.DataFrame):
    """Handle displaying most common key signatures."""
    print("\n" + "-" * 60)
    print("MOST COMMON KEY SIGNATURES")
    print("-" * 60)
    
    try:
        n = int(input("\nHow many top keys to display? (default 10): ") or "10")
        top_keys = get_most_common_keys(df, n)
        
        print(f"\n Top {n} Key Signatures:")
        for i, (key, count) in enumerate(top_keys.items(), 1):
            print(f"{i}. {key}: {count} tunes")
    except ValueError:
        print(" Invalid input. Please enter a number.")


def main_loop():
    """Main application loop."""
    print("\n" + "=" * 60)
    print(" WELCOME TO ABC TUNE DATABASE")
    print("=" * 60)
    
    # Load data once at startup
    print("\n Loading data from database...")
    df = load_tunes_from_database()
    
    if df is None:
        print(" Failed to load data. Exiting.")
        return
    
    print(f" Loaded {len(df)} tunes successfully!")
    
    # Main menu loop
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-9): ").strip()
        
        if choice == '1':
            handle_view_by_book(df)
        elif choice == '2':
            handle_search_by_type(df)
        elif choice == '3':
            handle_search_by_title(df)
        elif choice == '4':
            handle_search_by_key(df)
        elif choice == '5':
            handle_view_statistics(df)
        elif choice == '6':
            handle_view_tunes_per_book(df)
        elif choice == '7':
            handle_view_common_types(df)
        elif choice == '8':
            handle_view_common_keys(df)
        elif choice == '9':
            print("\n Thank you for using ABC Tune Database!")
            print("=" * 60)
            break
        else:
            print("\n Invalid choice. Please enter a number between 1 and 9.")
        
        # Pause before showing menu again
        input("\nPress Enter to continue...")


# Run the application
if __name__ == "__main__":
    main_loop()

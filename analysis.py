"""
Data analysis functions using pandas 
"""

import pandas as pd 
from database import connect_to_database
from typing import Optional


def load_tunes_from_database() -> Optional[pd.DataFrame]:
    """
    Load all tunes from MySQL into a pandas DataFrame

    Returns:
        dataframe containing all tune data and none if theres an error 

    Example:
        >>> df = load_tunes_from_database()
        >>> print(df.head())
    """
    conn = connect_to_database()

    if not conn:
        print("Failed to connect to the database")
        return None
    try:
        query = "SELECT * FROM tunes"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        conn.close()
        return None 
def get_tunes_by_book(df: pd.DataFrame, book_number: int) -> pd.DataFrame:
    """
    Get all tunes from a specific book

    Args: 
        df: DataFRame containing tune data
        book_number: Book number to filter by

    Returns:
        Filtered DataFrame
    
    Example:
        >>> df = load_tunes_from_database()
        >>> book_1_tunes = get_tunes_by_book(df, 1)
    """

    return df[df['book_number'] == book_number]

def get_tunes_by_type(df: pd.DataFrame, tune_type: str) -> pd.DataFrame:
    """
    Get all tunes of a specific type
    
    Args:
        df: DataFrame containing tune data
        tune_type: Type/rhythm to filter by (e.g., 'jig', 'reel', 'air')
        
    Returns:
        Filtered DataFrame
        
    Example:
        >>> df = load_tunes_from_database()
        >>> jigs = get_tunes_by_type(df, 'jig')
    """
    # Case-insensitive search
    return df[df['type'].str.contains(tune_type, case=False, na=False)]


def search_tunes(df: pd.DataFrame, search_term: str) -> pd.DataFrame:
    """
    Search for tunes by title (case-insensitive)
    
    Args:
        df: DataFrame containing tune data
        search_term: Term to search for in titles
        
    Returns:
        Filtered DataFrame
        
    Example:
        >>> df = load_tunes_from_database()
        >>> results = search_tunes(df, 'wind')
    """
    return df[df['title'].str.contains(search_term, case=False, na=False)]


def get_tunes_by_key(df: pd.DataFrame, key_signature: str) -> pd.DataFrame:
    """
    Get all tunes in a specific key
    
    Args:
        df: DataFrame containing tune data
        key_signature: Key signature to filter by (e.g., 'D', 'G', 'Am')
        
    Returns:
        Filtered DataFrame
        
    Example:
        >>> df = load_tunes_from_database()
        >>> d_major_tunes = get_tunes_by_key(df, 'D')
    """
    return df[df['key_signature'].str.contains(key_signature, case=False, na=False)]


def count_tunes_per_book(df: pd.DataFrame) -> pd.Series:
    """
    Count how many tunes are in each book
    
    Args:
        df: DataFrame containing tune data
        
    Returns:
        Series with book numbers and tune counts
        
    Example:
        >>> df = load_tunes_from_database()
        >>> counts = count_tunes_per_book(df)
        >>> print(counts)
    """
    return df['book_number'].value_counts().sort_index()


def get_most_common_types(df: pd.DataFrame, n: int = 10) -> pd.Series:
    """
    Get the most common tune types
    
    Args:
        df: DataFrame containing tune data
        n: Number of top types to return (default 10)
        
    Returns:
        Series with tune types and their counts
        
    Example:
        >>> df = load_tunes_from_database()
        >>> top_types = get_most_common_types(df, 5)
    """
    return df['type'].value_counts().head(n)


def get_most_common_keys(df: pd.DataFrame, n: int = 10) -> pd.Series:
    """
    Get the most common key signatures
    
    Args:
        df: DataFrame containing tune data
        n: Number of top keys to return (default 10)
        
    Returns:
        Series with key signatures and their counts
        
    Example:
        >>> df = load_tunes_from_database()
        >>> top_keys = get_most_common_keys(df, 5)
    """
    return df['key_signature'].value_counts().head(n)

def get_summary_statistics(df: pd.DataFrame) -> dict:
    """
    Get overall summary statistics about the tune collection

    Args: 
        df: DataFrame containing tune data
    
    Returns:
        Dictionary with various statistics
    
    Example:
        >>> df = load_tunes_from_database()
        >>> stats = get_summary_statistics(df)

    """

    stats = {
        'total_tunes': len(df),
        'total_books': df['book_number'].nunique(),
        'total_types': df['type'].nunique(),
        'total_keys': df['key_signature'].nunique(),
        'most_common_type': df['type'].mode()[0] if not df['type'].mode().empty else 'N/A',
        'most_common_key': df['key_signature'].mode()[0] if not df['key_signature'].mode().empty else 'N/A'
    }
    return stats

def export_to_pdf(df: pd.DataFrame, filename: str = "tunes_export.pdf") -> bool:
    """
    Exporting dataframe to a pdf file

    Args:
    df: DataFrame to export
    filename: Output PDF file

    Returns:
    true if successful fasle if not
    """

    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.units import inch

        # CReate PDF
        pdf = SimpleDocTemplate(filename, pagesize = A4)
        elements = []

        # Add title
        styles = getSampleStyleSheet()
        title = Paragraph("<b>ABC Tune Database Export</b>", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 0.2 * inch))

        # Add summary info
        summary = Paragraph(f"<b> Total Tunes:</b> {len(df)}", styles['Normal'])
        elements.append(summary)
        elements.append(Spacer(1, 0.2 * inch))

        # Select columns to display
        display_columns = ['id', 'book_number', 'title', 'type', 'key_signature', 'meter']
        df_display = df[display_columns].head(100) # limiting to first 100 for pdf

        # converting lists to lists for table
        data = [display_columns] + df_display.values.tolist()

        # Create table
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        
        # Build PDF
        pdf.build(elements)

        print(f"PDF exported successfully: {filename}")
        return True
    
    except ImportError:
        print("reportlab not installed. install with: pip install reportlab")
        return False
    except Exception as e:
        print(f"Error exporting PDF: {e}")
        return False
    
# Test the analysis functions
if __name__ == "__main__":
    print("Testing Analysis Functions")
    print("=" * 60)
    
    # Load data
    print("\n[1] Loading data from database...")
    df = load_tunes_from_database()
    
    if df is not None:
        print(f" Loaded {len(df)} tunes")
        print(f"\nDataFrame Info:")
        print(df.info())
        
        # Test summary statistics
        print("\n[2] Summary Statistics:")
        print("-" * 60)
        stats = get_summary_statistics(df)
        for key, value in stats.items():
            print(f"{key}: {value}")
        
        # Test tune counts per book
        print("\n[3] Tunes per Book:")
        print("-" * 60)
        print(count_tunes_per_book(df))
        
        # Test most common types
        print("\n[4] Top 10 Tune Types:")
        print("-" * 60)
        print(get_most_common_types(df, 10))
        
        # Test most common keys
        print("\n[5] Top 10 Key Signatures:")
        print("-" * 60)
        print(get_most_common_keys(df, 10))
        
        # Test search
        print("\n[6] Search for 'reel':")
        print("-" * 60)
        results = search_tunes(df, 'reel')
        print(f"Found {len(results)} tunes with 'reel' in title")
        print(results[['title', 'type', 'key_signature']].head())
        
    else:
        print(" Failed to load data")
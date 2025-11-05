"""
File Loader and Traversing functions for ABC tune files
"""
from typing import List, Tuple
import os

def find_abc_files(root_dir: str) -> List[Tuple[int, str]]:
    """
    Recursively find all ABC files in directory structure.

    Args: 
            root_dir: Path to the abc_books directory
    
    Returns: 
            List of tuples (book_number, file_path)

    Eg: 
        >>> files = find_abc_files('abc_books/')
        >>> print(files[0])
        (0, 'abc_books/0/tune001.abc') 
    """
    abc_files = []

    # Directory structure 
    for folder_name in os.listdir(root_dir):
        folder_path = os.path.join(root_dir, folder_name)

        # Check if it's a directory and the name is a number 
        if os.path.isdir(folder_path) and folder_name.isdigit():
            book_number = int(folder_name)

            # find all .abc files in this folder 
            for file_name in os.listdir(folder_path):
                if file_name.endswith('.abc'):
                    file_path = os.path.join(folder_path, file_name)
                    abc_files.append((book_number, file_path))

    return abc_files

# test the function if running this file directly
if __name__ == "__main__":
    files = find_abc_files('abc_books')
    print(f"Found {len(files)} ABC files:")
    for book_num, file_path in files[:5]: # shows the first five
        print(f"  Book {book_num}: {file_path}")
"""
ABC file parsing functions
"""
from typing import List, Dict  # importing lists and dicts for type hinting
import re  # regular expression operations for splitting tunes


def parse_abc_file(file_path: str) -> List[Dict[str, str]]:
    """
    Parse an ABC file and extract all tunes.

    Args: 
        file_path: Path to the ABC file

    Returns:
        List of dictionaries, each containing tune metadata and notations

    Example:
        >>> tunes = parse_abc_file('abc_books/1/hnair0.abc')
        >>> print(tunes[0]['title'])
        'Down the Hill'
    """
    tunes = []

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Split by X: to separate tunes (X: marks the start of each tune)
        tune_sections = re.split(r'\n(?=X:)', content)

        for section in tune_sections:
            # Skip empty sections or sections without X:
            if not section.strip() or not section.strip().startswith('X:'):
                continue
            
            # Parse this tune and add it to the list
            tune_dict = parse_single_tune(section)
            if tune_dict:
                tunes.append(tune_dict)

    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
    
    return tunes


def parse_single_tune(tune_text: str) -> Dict[str, str]:
    """
    Parse a single tune's ABC notation.

    Args:
        tune_text: ABC notation text for one tune

    Returns:
        Dictionary with tune metadata
    """
    tune_dict = {
        'reference_number': '',
        'title': '',
        'type': '',
        'meter': '',
        'key': '',
        'abc_notation': tune_text
    }
    
    lines = tune_text.split('\n')

    for line in lines:
        line = line.strip()

        # Reference number (X:)
        if line.startswith('X:'):
            tune_dict['reference_number'] = line[2:].strip()

        # Title (T:) - take the first one if multiple 
        elif line.startswith('T:') and not tune_dict['title']:
            tune_dict['title'] = line[2:].strip()

        # Type/Rhythm (R:)
        elif line.startswith('R:'):
            tune_dict['type'] = line[2:].strip()

        # Meter (M:)
        elif line.startswith('M:'):
            tune_dict['meter'] = line[2:].strip()
        
        # Key (K:)
        elif line.startswith('K:'):
            tune_dict['key'] = line[2:].strip()

    return tune_dict


# Test the parser
if __name__ == "__main__":
    test_file = 'abc_books/1/hnair0.abc'
    
    with open(test_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    print(f"File has {len(content)} characters")
    
    # Try the split
    tune_sections = re.split(r'\n(?=X:)', content)
    print(f"Number of sections after split: {len(tune_sections)}")
    
    # Check first few sections
    for i in range(min(3, len(tune_sections))):
        section = tune_sections[i]
        print(f"\n--- Section {i} (first 100 chars) ---")
        print(section[:100])
        print(f"Starts with 'X:'? {section.strip().startswith('X:')}")
    
    # Now run the actual parser
    print("\n\n=== Running Parser ===")
    tunes = parse_abc_file(test_file)
    
    print(f"Found {len(tunes)} tunes")
    for i, tune in enumerate(tunes[:3]):
        print(f"\n{i+1}. Title: {tune['title']}")
        print(f"   Type: {tune['type']}")
        print(f"   Key: {tune['key']}")
        print(f"   Meter: {tune['meter']}")

    
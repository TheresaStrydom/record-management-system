import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import pytest
from storage import load_records, save_records

@pytest.fixture
def temp_file():
    file_path = '../test_records.json'  # Temp file in root to avoid overwriting real data
    if os.path.exists(file_path):
        os.remove(file_path)
    yield file_path
    if os.path.exists(file_path):
        os.remove(file_path)

def test_load_nonexistent(temp_file):
    """Test loading from a non-existent file returns empty list."""
    assert load_records(temp_file) == []

def test_save_load(temp_file):
    """Test saving and loading preserves the records."""
    test_records = [
        {
            "ID": 1,
            "Type": "Client",
            "Name": "Test Client",
            "Address Line 1": "123 Test St",
            "Address Line 2": "",
            "Address Line 3": "",
            "City": "Test City",
            "State": "TS",
            "Zip Code": "12345",
            "Country": "Testland",
            "Phone Number": "555-1234"
        }
    ]
    save_records(test_records, temp_file)
    loaded = load_records(temp_file)
    assert loaded == test_records

def test_load_corrupted(temp_file):
    """Test loading a corrupted file returns empty list without crashing."""
    # Simulate corrupted file
    with open(temp_file, 'w') as f:
        f.write("invalid json")
    assert load_records(temp_file) == []

import pytest
import os
from src.storage import load_records, save_records

@pytest.fixture
def temp_file():
    file_path = os.path.join(os.path.dirname(__file__), '../test_records.json')
    if os.path.exists(file_path):
        os.remove(file_path)
    yield file_path
    if os.path.exists(file_path):
        os.remove(file_path)

def test_load_nonexistent(temp_file):
    """Test loading from a non-existent file returns empty nested dict."""
    assert load_records(temp_file) == {"Clients": [], "Airlines": [], "Flights": []}

def test_save_load(temp_file):
    """Test saving and loading preserves the nested records."""
    test_records = {
        "Clients": [
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
        ],
        "Airlines": [],
        "Flights": []
    }
    save_records(test_records, temp_file)
    loaded = load_records(temp_file)
    assert loaded == test_records

def test_load_corrupted(temp_file):
    """Test loading a corrupted file returns empty nested dict without crashing."""
    # Simulate corrupted file
    with open(temp_file, 'w') as f:
        f.write("invalid json")
    assert load_records(temp_file) == {"Clients": [], "Airlines": [], "Flights": []}
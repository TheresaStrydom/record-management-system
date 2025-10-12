import json
import os

def load_records(file_path='../records.json'):
    """
    Load the nested records from a JSON file if it exists.
    Returns an empty dict if the file doesn't exist or is corrupted.
    """
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Error: Corrupted JSON file. Starting with an empty dict.")
            return {"Client": [], "Airline": [], "Flight": []}
        except Exception as e:
            print(f"Error loading records: {e}")
            return {"Client": [], "Airline": [], "Flight": []}
    else:
        print("No records file found. Starting with an empty dict.")
    return {"Client": [], "Airline": [], "Flight": []}

def save_records(records, file_path='../records.json'):
    """
    Save the nested records dict to a JSON file.
    Overwrites the file if it exists.
    """
    try:
        with open(file_path, 'w') as f:
            json.dump(records, f, indent=4)
        print("Records saved successfully.")
    except Exception as e:
        print(f"Error saving records: {e}")

# Simple test block to verify functionality standalone
# Run this file directly: python src/storage.py
if __name__ == "__main__":
    # Sample nested records
    test_records = {
        "Client": [
            {
                "ID": 1,
                "Type": "Client",
                "Name": "John Doe",
                "Address Line 1": "123 Main St",
                "Address Line 2": "",
                "Address Line 3": "",
                "City": "New York",
                "State": "NY",
                "Zip Code": "10001",
                "Country": "USA",
                "Phone Number": "123-456-7890"
            }
        ],
        "Airline": [
            {
                "ID": 1,
                "Type": "Airline",
                "Company Name": "FlyHigh Airlines"
            }
        ],
        "Flight": [
            {
                "Client_ID": 1,
                "Airline_ID": 1,
                "Date": "2025-10-15T10:00:00",
                "Start City": "New York",
                "End City": "Los Angeles"
            }
        ]
    }
    
    # Test save
    save_records(test_records)
    
    # Test load
    loaded_records = load_records()
    print("Loaded records:")
    print(loaded_records)
    
    # Quick check
    if loaded_records == test_records:
        print("Test passed: Saved and loaded records match.")
    else:
        print("Test failed: Mismatch in records.")

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import pytest
from records import create_record, search_records, update_record, delete_record

@pytest.fixture
def temp_file():
    file_path = '../test_records.json'
    if os.path.exists(file_path):
        os.remove(file_path)
    yield file_path
    if os.path.exists(file_path):
        os.remove(file_path)

def test_crud_operations(temp_file):
    """Test basic CRUD operations on records."""
    # Start with empty records dict
    records = {"Client": [], "Airline": [], "Flight": []}

    # CREATE
    new_record = {
        "Name": "CRUD Client",
        "Address Line 1": "456 CRUD St",
        "Address Line 2": "",
        "Address Line 3": "",
        "City": "CRUD City",
        "State": "CR",
        "Zip Code": "67890",
        "Country": "CRUDland",
        "Phone Number": "555-6789"
    }
    create_result = create_record(records, new_record, "Client")
    # The function returns a string, so check the result
    assert create_result == "Entry has been created successfully"
    # The new record should now be in records["Client"]
    assert any(r["Name"] == "CRUD Client" for r in records["Client"])

    # READ
    # Get the ID of the created client
    created_id = records["Client"][0]["ID"]
    found = search_records(records, str(created_id), "Client")
    assert isinstance(found, list)
    assert found[0]["Name"] == "CRUD Client"

    # UPDATE
    update_result = update_record(records, "Client", {"Name": "Updated Client"}, client_id=str(created_id))
    assert update_result == 1
    assert records["Client"][0]["Name"] == "Updated Client"

    # DELETE
    delete_result = delete_record(records, "Client", client_id=str(created_id))
    assert delete_result is None or delete_result == 0  # Your function returns None on success
    assert not records["Client"]  # Should be empty now

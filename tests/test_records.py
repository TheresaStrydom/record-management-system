import pytest
import json
import src.records as records

@pytest.fixture
def mock_records():
    return {
        "Client": [
            {"ID":1, "Type":"Client","Name":"John Doe"},
            {"ID":2, "Type":"Client","Name":"Nic Moe"}
        ],
        "Airline": [
            {"ID":1, "Type":"Airline","Company Name":"British Airways"},
            {"ID":2, "Type":"Airline","Company Name":"American Airlines"},
        ], 
        "Flight": [
            {"Client_ID":1,"Airline_ID":1,"Type":"Flight","Date":"2025-10-01T10:00:00","Start City":"Berlin","End City":"London"},
            {"Client_ID":2,"Airline_ID":2,"Type":"Flight","Date":"2025-11-03T12:30:00","Start City":"Juarez","End City":"El Paso"}
        ] 
    }
 
 # Test for search_records()
def test_search_by_type_valid(mock_records):    # Proves that the mocks_records are valid
    result = records.search_records(mock_records, type_search="Client")  
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["Name"] == "John Doe"

def test_search_by_type_invalid(mock_records, capsys):  # Proves that the code can handle searching an invalid type
    result = records.search_records(mock_records, type_search="Invalid")
    captured = capsys.readouterr()
    assert "Invalid Type" in captured.out

def test_search_by_id_valid(mock_records,capsys):   # Proves that the code can handle searching an valid IDs
    result = records.search_records(mock_records, id_search=1)
    captured = capsys.readouterr()
    assert "John Doe" in captured.out     
    assert "British Airways" in captured.out

def test_search_by_id_invalid(mock_records,capsys):   # Proves that the code can handle searching an invalid IDs
    result = records.search_records(mock_records, id_search=13)
    captured = capsys.readouterr()
    assert "ID not found" in captured.out     
    
def test_search_by_id_and_type_valid(mock_records,capsys):  # Proves that the code can handle searching valid ID and types
    result = records.search_records(mock_records, id_search=1,type_search="Flight")
    captured = capsys.readouterr()
    assert "Berlin" in captured.out

def test_search_by_id_and_type_invalid(mock_records,capsys):  # Proves that the code can handle searching invalid ID and types
    result = records.search_records(mock_records, id_search=17,type_search="Flight")
    captured = capsys.readouterr()
    assert "Invalid ID" in captured.out

 # Test for create_record()
def test_create_record_valid_flight(mock_records,capsys): # Proves that the code can handle creating a valid flight
    new_flight = {
        "Client_ID":1,
        "Airline_ID":52,
        "Type":"Flight",
        "Date":"2025-04-03T08:15:00",
        "Start City":"Las Cruses",
        "End City":"Los Angeles"
    }
    result = records.create_record(mock_records,new_flight,"Flight")
    captured = capsys.readouterr()
    assert "Las Cruses" in captured.out
    assert len(mock_records["Flight"]) == 2

def test_create_record_invalid_client(mock_records,capsys):     # Proves that the code can handle creating an invalid client
    new_flight = {
        "Client_ID":1,
        "Airline_ID":52,
        "Type":"Flight",
        "Date":"2025-04-03T08:15:00",
        "Start City":"Las Cruses",
        "End City":"Los Angeles"
    }
    result = records.create_record(mock_records,new_flight,"Flight")
    captured = capsys.readouterr()
    assert "Invalid Client_ID" in captured.out    

def test_create_record_valid_client(mock_records,capsys):     # Proves that the code can handle creating a valid client
    new_client = {
        "Name":"Nicola Smith",
        "Address Line 1":"1 Flag Lane",
        "City":"Leeds",
        "State":"West Yorkshire",
        "Zip Code":"LS1 6PT",
        "Country":"England",
        "Phone Number":"0789153458"
    }
    result = records.create_record(mock_records,new_client,"Client")
    captured = capsys.readouterr()
    assert "Entry has been created" in captured.out

def test_create_record_invalid_type(mock_records,capsys): # Proves that the code can handle creating a invalid type
    result = records.create_record(mock_records,{"data":"test"},"unknowntype")
    captured = capsys.readouterr()
    assert "Invalid Type" in captured.out

def test_update_record_valid_client(mock_records, capsys):    # Proves that the code can handle updating an existing valid client
    updated_client = {
        "Type":"Client",
        "ID":1,
        "Name":"Johnathan Doe",
        "Phone Number":"9155559999"
    }
    result = records.update_record(mock_records,1, "Client")
    captured = capsys.readouterr()
    assert "Entry has been updated successfully" in captured.out
    assert any(c["Name"] == "Johnathan Doe" for c in mock_records["Client"])

def test_update_record_invalid_type(mock_records, capsys):      # Proves that the code can handle updating invalic record type
    updated_data = {"ID":1, "Name":"Oscar Len"}
    result = records.update_record(mock_records, updated_data, "Unknown Type") 
    captured = capsys.readouterr()
    assert "Invalid Type" in captured.out

def test_update_record_invalid_id(mock_records, capsys):    # Proves that code can handle updating an ID that does not exist
    updated_client = {
        "ID":43,
        "Name": "Terry Cruz"
    }
    result = records.update_record(mock_records, updated_client, "Client")
    captured = capsys.readouterr
    assert "ID not found" in captured.out

def test_update_record_valid_flight(mock_records, capsys):  # Proves that code can handle updating an existing flight
    updated_flight = {
        "Client_ID": 1,
        "Airline_ID": 1,
        "Type": "Flight",
        "Date": "2025-10-01T10:00:00",
        "Start City": "Berlin",
        "End City": "Paris"
    }
    result = records.update_record(mock_records, updated_flight, "Flight")
    captured = capsys.readouterr()
    assert "Record updated successfully" in captured.out
    assert any(f["End City"] == "Paris" for f in mock_records["Flight"])



    # Delete Record
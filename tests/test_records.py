import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import src.records as records
import pytest
import json

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
def test_search_by_type_valid(mock_records):    # Searching a valid type
    result = records.search_records(mock_records,"1", type_search="Client")  
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["Name"] == "John Doe"

def test_search_by_type_invalid(mock_records, capsys):  # Searching an invalid type
    result = records.search_records(mock_records,"1", type_search="Invalid")
    assert result == -2

def test_search_by_id_valid(mock_records,capsys):   # Searching an valid ID
    client_result = records.search_records(mock_records,"1", type_search="Client")
    airline_result = records.search_records(mock_records,"1", type_search="Airline")
    all_results = (client_result or []) + (airline_result or [])
    for record in all_results:
        print(record)
    captured = capsys.readouterr()
    assert "John Doe" in captured.out     
    assert "British Airways" in captured.out

def test_search_by_id_invalid(mock_records,capsys):   # Searching an invalid ID
    result = records.search_records(mock_records,"13", type_search="Client")
    captured = capsys.readouterr()
    assert result == -1    
    
def test_search_by_id_and_type_valid(mock_records,capsys):  # Searching valid ID and type
    result = records.search_records(mock_records, id_search="1",type_search="Flight")
    captured = capsys.readouterr()
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["Start City"] == "Berlin"
    assert result[0]["End City"] == "London"

def test_search_by_id_and_type_invalid(mock_records,capsys):  # Searching invalid ID and type
    result = records.search_records(mock_records, id_search="17",type_search="Flight")
    captured = capsys.readouterr()
    assert result == -1

def test_search_by_type_flight(mock_records): # Searching valid flight
    result = records.search_records(mock_records, id_search="1", type_search="Flight")
    assert isinstance(result, list)
    assert any(f["Start City"] == "Berlin" for f in result)

def test_search_by_type_invalid_flight(mock_records):   # Searching invalid Flight 
    result = records.search_records(mock_records, id_search="99", type_search="Flight")
    assert result == -1

 # Test for create_record()
def test_create_record_valid_flight(mock_records,capsys): # Creating a valid flight
    new_flight = {
        "Client_ID":1,
        "Airline_ID":1,
        "Type":"Flight",
        "Date":"2025-04-03T08:15:00",
        "Start City":"Las Cruses",
        "End City":"Los Angeles"
    }
    result = records.create_record(mock_records,new_flight,"Flight")
    captured = capsys.readouterr()
    assert any(f["Start City"] == "Las Cruses" for f in mock_records["Flight"])
    assert len(mock_records["Flight"]) == 3

def test_create_record_invalid_flight(mock_records,capsys):     # Creating an invalid flight
    new_flight = {
        "Client_ID":1,
        "Airline_ID":52,
        "Type":"Flight",
        "Date":"2025-04-03T08:15:00",
        "Start City":"Las Cruses",
        "End City":"Los Angeles"
    }
    result = records.create_record(mock_records,new_flight,"Flight")
    assert result == -1   

def test_create_record_valid_client(mock_records,capsys):     # Creating a valid client
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
    assert result == "Entry has been created successfully"
    assert any(c["Name"] == "Nicola Smith" for c in mock_records["Client"])

def test_create_record_invalid_type(mock_records,capsys): # Creating a invalid type
    result = records.create_record(mock_records,{"data":"test"},"unknowntype")
    captured = capsys.readouterr()
    assert result == -2

def test_create_record_valid_airline(mock_records): # Creating a valid airline
    new_airline = {
        "Company Name": "Delta Airlines"
    }
    result = records.create_record(mock_records, new_airline, "Airline")
    assert result == "Entry has been created successfully"
    assert any(a["Company Name"] == "Delta Airlines" for a in mock_records["Airline"])



#Test for update record
def test_update_record_valid_client(mock_records, capsys):    # Updating an existing valid client
    updated_client = {
        "Type":"Client",
        "ID":1,
        "Name":"Johnathan Doe",
        "Phone Number":"9155559999"
    }
    result = records.update_record(mock_records,"Client", updated_client,client_id="1")
    captured = capsys.readouterr()
    assert result == 1
    updated = next((c for c in mock_records["Client"] if c["ID"] == 1), None)
    assert updated["Name"] == "Johnathan Doe"
    assert updated["Phone Number"] == "9155559999"

def test_update_record_invalid_client_id(mock_records):     # Updating a client with an invalid ID
    updated_client = {"Name": "Invalid Person"}
    result = records.update_record(mock_records, "Client", updated_client, client_id="99")
    assert result == -1

def test_update_record_invalid_type(mock_records, capsys):      # Updating invalid type
    updated_client = {
        "Type":"Client",
        "ID":99,
        "Name":"Johnathan Doe",
        "Phone Number":"9155559999"
    }
    result = records.update_record(mock_records,"UnknownType", updated_client)
    assert result == -2


def test_update_record_valid_flight(mock_records, capsys):   # Updating an existing valid flight
    updated_flight = {"End City": "Paris"}
    result = records.update_record(mock_records, "Flight", updated_flight, client_id="1", airline_id="1")
    captured = capsys.readouterr()
    assert result == 1
    updated = next((f for f in mock_records["Flight"] if f["Client_ID"] == 1 and f["Airline_ID"] == 1), None)
    assert updated["End City"] == "Paris"

def test_update_record_invalid_airline_id(mock_records):   # Updating invalid airline ID 
    updated_airline = {"Company Name": "Nike"}
    result = records.update_record(mock_records, "Airline", updated_airline, airline_id="107")
    assert result == -1    

#Test for delete record
def test_delete_record_valid_client(mock_records,capsys):   # Deleting an exisiting valid client
    result = records.delete_record(mock_records,"Client",client_id="1")
    captured = capsys.readouterr()
    assert all(c["ID"] != 1 for c in mock_records["Client"])
    assert len(mock_records["Client"]) == 1

def test_delete_record_invalid_client(mock_records):        # Deleting invalid client 
    result = records.delete_record(mock_records, "Client", client_id="57")
    assert result is None
    assert len(mock_records["Client"]) == 2 

def test_delete_record_valid_flight(mock_records,capsys):   # Deleting an exisiting valid flight
    result = records.delete_record(mock_records,"Flight",client_id="1",airline_id="1")
    captured = capsys.readouterr()
    assert all(
        not (f["Client_ID"] == 1 and f["Airline_ID"] == 1)
        for f in mock_records["Flight"]
    )
    assert len(mock_records["Flight"]) == 1

def test_delete_record_invalid_airline(mock_records):    # Deleting invalid airline
    result = records.delete_record(mock_records, "Airline", airline_id="103")
    assert result is None
    assert len(mock_records["Airline"]) == 2

def test_delete_record_invalid_type(mock_records):      # Deleting an invalid type
    result = records.delete_record(mock_records,"Invalid Type")
    assert result == -2


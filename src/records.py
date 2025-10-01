"""
This module has to create the CRUD functions by validating information from the GUI

Searching for records.
Creating records.
Updating records.
Deleting records

And ensures referential integrity
"""

import json
from pickle import GLOBAL

with open("records.json",'r') as file:
    records = json.load(file)

new_client = {
    "ID": 3,
    "Type": "Client",
    "Name": "Sarah Connor",
    "Address Line 1": "321 Future St",
    "Address Line 2": "",
    "Address Line 3": "",
    "City": "San Francisco",
    "State": "CA",
    "Zip Code": "94101",
    "Country": "USA",
    "Phone Number": "+1-555-444-5555"
}
data_1 = new_client

new_new_client = {

    "Name": "Sarah Connor",
    "Address Line 1": "321 Future St",
    "Address Line 2": "",
    "Address Line 3": "",
    "City": "San Francisco",
    "State": "CA",
    "Zip Code": "94101",
    "Country": "USA",
    "Phone Number": "+1-555-444-5555"
}
data_4 = new_new_client
new_airline = {
    "ID": 3,
    "Type": "Airline",
    "Company Name": "British Airways"
}

new_1_airline = {
    "Company Name": "British Airways"
}

data_5 = new_1_airline

data_2 = new_airline

# Build check class?

new_flight = {
    "Client_ID": 1,
    "Airline_ID": 1,
    "Type": "Flight",
    "Date": "2025-10-01T14:30:00",
    "Start City": "Cape Town",
    "End City": "New York"
        }

data_3 = new_flight



def search_records(records_json, id_search=None,type_search=None):
    """
    This function searches the json list using a specific id and type
    :param records_json: the json object
    :param id_search: the identification number of the record
    :param type_search: the entry type,
    :return: the result of the search
    """

    # Searches the list if only the Type is passed
    result = []
    if id_search is None:
        if type_search in records_json:
            for element in records_json[type_search]:
                result.append(element)
            return result
        else:
            return print("Invalid Type")
    # Searches the list if only the ID is passed
    elif type_search is None:
        for element, items in records_json.items():
           for field in items:
               if field.get('ID') == id_search:
                   result.append(field)
               if field.get("Client_ID") == id_search or field.get("Airline_ID") == id_search:
                   result.append(field)
        if not result:
            return print("ID not found")
        else:
            return print(result)
    # Searches the list if both the ID and Type are passed
    elif type_search is not None and id_search is not None:
        if type_search in records_json:
            for element in records_json[type_search]:
                if element.get("ID") == id_search:
                    result.append(element)
                if element.get("Client_ID") == id_search or element.get("Airline_ID") == id_search:
                    result.append(element)
            if not result:
                return print("Invalid ID")
            else:
                return print(result)
        else:
            return print("Invalid Type")
    else:
        return print("Invalid parameters")

def create_record(records_json, data,type_create):
    """
    This function creates a new entry in the json object
    :param records_json: the json object
    :param data: a list of data that needs to be added to the json object
    :param type_create: the type of record that needs to be created
    :return: result of creation
    """

#Need to know how many elements are passed in data for validation

    global client, airline

    if type_create == 'Flight':
        # Test if the Client_ID in data is in the json record
        for element in records_json["Client"]:
            if element.get("ID") == data.get("Client_ID"):
                client = True
                break
            else:
                client = False
        # Test if the Airline_ID in data is in the json record
        for element in records_json["Airline"]:
            if element.get("ID") == data.get("Airline_ID"):
                airline = True
                break
            else:
                airline = False
        # Test the result and append Flights
        if client is False:
            return print("Invalid Client_ID")
        elif airline is False:
            return print("Invalid Airline_ID")
        else:
            records_json['Flight'].append(data)
            return print(records_json["Flight"])

    # Test the type_create in the json record, if so, append
    elif type_create in records_json:
        if records_json[type_create] == [{}]:
            max_id = 0
        else:
            max_id = max(type_create["ID"] for type_create in records_json[type_create])

        updates_data = {'ID': max_id + 1, 'Type':type_create}
        updates_data.update(data)
        records_json[type_create].append(updates_data)
    else:
        return print("Invalid type")
    # Tests if the new record has been updated successfully
    if records_json[type_create][-1] == updates_data:
        return print("Entry has been created successfully")
    else:
        return print("Entry has not been created")     # Return Depends on call.

def update_record(records_json,id_update,data):
    """
    This function modifies an existing record in the json object
    :param records_json: the json object
    :param id_update: the identification number of the record to update
    :param data: a list of data to update the entry with
    :return: the result of the update
    """
    element_type = data["Type"]
    id_pos = id_update-1

    for element in records_json[element_type][id_pos]:
        updates_data = {element:data[element]}
        records_json[element_type][id_pos].update(updates_data) # if an empty data is passed then the update will also be empty

    if records_json[element_type][id_pos] == data:
         return "Entry has been updated successfully"
    else:
        return "Entry has not been updated"



def delete_record(records_json,id_delete,delete_type):
    """
    This function deletes an existing record in the json object
    :param delete_type: the type of record that will be recorded
    :param records_json: the json object
    :param id_delete: the identification number of the record to delete

    :return: the result of the json manipulation
    """
    if delete_type == 'Flight':
        records_json[delete_type] = [element for element in records_json[delete_type] if
                                     element["Client_ID"] != id_delete] # Can put OR for airline ID
    else:
        if delete_type in records_json:
            records_json[delete_type] = [element for element in records_json[delete_type] if
                                         element["ID"] != id_delete]
        else:
            return None
    return print(records_json[delete_type])
    # if flights then it takes the client ID the GUI may have to request the Client_ID.

#create_record(records, data_5,'Client')
#create_record(records,data_2,"Airline")
#print(create_record(records,data_3,"Flight"))
#print(records["Clients"])
#update_record(records,1,data_1)
#update_record(records,3,data_3)
#delete_record(records, 1, "Flight")
#search_records(records,4, "Flight" )
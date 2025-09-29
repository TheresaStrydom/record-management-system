"""
This module has to create the CRUD functions by validating information from the GUI

Searching for records.
Creating records.
Updating records.
Deleting records

And ensures referential integrity
"""

import json

with open("record.jsonl",'r') as file:
    records = json.load(file)

new_client = {
    "ID": 2,
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

new_airline = {
    "ID": 3,
    "Type": "Airline",
    "Company Name": "British Airways"
}

data_2 = new_airline

# Build check class?

new_flight = {
    "Client_ID": 2,
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
    if type_search == 'Client':
        for client in records_json["Client"]:
            if client["ID"] == id_search:
                return print(client)
        return None
    elif type_search == 'Airline':
        for airline in records_json["Airline"]:
            if airline["ID"] == id_search:
                return print(airline)
        return None
    elif type_search == 'Flight':
        for flight in records_json["Flight"]:
            if flight["Client_ID"] == id_search:
                return print(flight)
        return None
    else:
        print("Invalid type")
        return None


def create_record(records_json, data,type_create):
    """
    This function creates a new entry in the json object
    :param records_json: the json object
    :param data: a list of data that needs to be added to the json object
    :param type_create: the type of record that needs to be created
    :return: result of creation
    """
    if type_create == 'Flight':
        records_json['Flight'].append(data) # NB! Dependent on what is passed to the data file.
        if records_json[type_create][-1]== data:
            return "Entry has been updated successfully"
        else:
            return "Entry has not been update successfully"
    else:
        if records_json[type_create]:
            max_id = max(type_create["ID"]for type_create in records_json[type_create])
        else:
            max_id = 0
        updates_data = {'ID': max_id + 1, 'Type':type_create}
        updates_data.update(data)
        records_json[type_create].append(updates_data)

        if records_json[type_create][-1]== updates_data:
            return "Entry has been created successfully"
        else:
            return "Entry has not been created"     #Depends on call.

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
        records_json[element_type][id_pos].update(updates_data)

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
                                     element["Client_ID"] != id_delete]
    else:
        if delete_type in records_json:
            records_json[delete_type] = [element for element in records_json[delete_type] if
                                         element["ID"] != id_delete]
        else:
            return None
    return print(records_json[delete_type])
    # if flights then it takes the client ID the GUI may have to request the flight ID.

#search_records(records, 2, "Flights")
#create_record(records, data_1,'Clients')
#create_record(records,data_2,"Airlines")
#print(create_record(records,data_3,"Flights"))

#print(records["Clients"])
#update_record(records,1,data_1)
#update_record(records,3,data_3)
#with open("record.jsonl",'w') as file:
#    json.dump(records,file, indent=4)

# print(element,data[element],"....",records_json[element_type][id_pos][element])
delete_record(records, 1, "Flight")
"""
This module has to create the CRUD functions by validating information from the GUI

Searching for records.
Creating records.
Updating records.
Deleting records

And ensures referential integrity
"""

import re

def validate_input(passed_id):
    """
    This function validates that the passed ID is numerical value and casts
    it to a string if it is or
    returns -1 if it fails.
    :param passed_id: The id passed by GUI
    :return: either the integer value or -1 for failure
    """
    if bool(re.fullmatch(r'\d+',passed_id)):
        passed_id = int(passed_id)
        return passed_id
    return -1


def search_records(records_json, id_search , type_search):   # Changed default
    """
    This function searches the json list using a specific id and type
    :param records_json: the json object
    :param id_search: the identification number of the record
    :param type_search: the entry type,
    :return: the result of the search
    """
    result = []

    id_search = validate_input(id_search)

    if id_search != -1:
    # Searches the list if only the Type is passed
        if type_search in records_json:
            for element in records_json[type_search]:
                if element.get("ID") == id_search or element.get("Client_ID") == id_search:
                    try:
                        result.append(element)
                    except AttributeError:
                        print("Error: Record in not a Json object")
                    except TypeError:
                        print("Error: Data must be a Json object")
            if not result:
                 # ID Not Found
                return -1
            return result
        # Invalid Type
        return -2
    return id_search # Invalid ID

def create_record(records_json, data, type_create):
    """
    This function creates a new entry in the json object
    :param records_json: the json object
    :param data: a list of data that needs to be added to the json object
    :param type_create: the type of record that needs to be created
    :return: result of creation
    """

    global client, airline

    if type_create == 'Flight':
        # Test if the Client_ID in data is in the json record
        for element in records_json["Client"]:
            if element.get("ID") == data.get("Client_ID"):
                client = True
                break
            client = False
        # Test if the Airline_ID in data is in the json record
        for element in records_json["Airline"]:
            if element.get("ID") == data.get("Airline_ID"):
                airline = True
                break
            airline = False
        # Test the result and append Flights
        if client is False:
            return -1 # Invalid ID
        if airline is False:
            return -1 # Invalid ID
        try:
            records_json['Flight'].append(data)
        except AttributeError:
            print("Error: Record in not a Json object")
        except TypeError:
            print("Error: Data must be a Json object")
        return print(records_json["Flight"])

    # Test the type_create in the json record, if so, append
    if type_create in records_json:
        if records_json[type_create] == [{}]:
            max_id = 0
        else:
            max_id = max(r["ID"] for r in records_json[type_create])

        updates_data = {'ID': max_id + 1, 'Type':type_create}
        try:
            updates_data.update(data)
            records_json[type_create].append(updates_data)
        except AttributeError:
            print("Error: Record in not a Json object")
        except TypeError:
            print("Error: Data must be a Json object")
    else:
        return -2 # INVALID TYPE

    # Tests if the new record has been updated successfully
    if if records_json[type_create][-1] == updates_data:
        return "Entry has been created successfully"
    return "Entry has not been created"

def update_record(records_json, type_update, data, client_id=None, airline_id =None):
    """
    This function modifies an existing record in the json object
    :param client_id: The ID of the client
    :param airline_id: The ID of the airline
    :param records_json: the json object
    :param type_update: the identification number of the record to update
    :param data: a list of data to update the entry with
    :return: the result of the update
    """

    if type_update == 'Client':
        # Test if the Client_ID in data is in the json record and updates record
        client_id = validate_input(client_id)
        if client_id != -1:
            for element in records_json["Client"]:
                if element.get("ID") == client_id:
                    try:
                        element.update(data)
                    except AttributeError:
                        print("Error: Record in not a Json object")
                    except TypeError:
                        print("Error: Data must be a Json object")
                    return 1 # Successful update
                # ID NOT FOUND
                return  -1
        else:
            return client_id # Invalid ID

    elif type_update == "Airline":
        # Test if the Airline_ID in data is in the json record and updates record
        airline_id =  validate_input(airline_id)
        if airline_id != -1:
            for element in records_json["Airline"]:
                if element.get("ID") == airline_id:
                    try:
                        element.update(data)
                    except AttributeError:
                        print("Error: Record in not a Json object")
                    except TypeError:
                        print("Error: Data must be a Json object")
                    return 1 # Successful update
                # ID NOT FOUND
                return -1
        else:
            return airline_id # Invalid ID

    elif type_update == "Flight":

        # Test if the Airline_ID and Client_ID in data in the Json record and updates record
        client_id = validate_input(client_id)
        airline_id = validate_input(airline_id)

        if client_id != -1 and airline_id != -1:
            for element in records_json["Flight"]:
                if (element.get("Client_ID") == client_id and
                        element.get("Airline_ID") == airline_id):
                    try:
                        element.update(data)
                    except AttributeError:
                        print("Error: Record in not a Json object")
                    except TypeError:
                        print("Error: Data must be a Json object")
                    return 1 # Successful update
                return -1 # IDs NOT FOUND
    else:
        return -2 # TYPE NOT FOUND

def delete_record(records_json,type_delete, client_id=None, airline_id = None):
    """
    This function deletes an existing record in the json object
    :param airline_id: The ID of the airline
    :param type_delete: the type of record that will be deleted
    :param records_json: the json object
    :param client_id: The ID of the client

    :return: the result of the json manipulation
    """
    if type_delete == 'Flight':
        client_id = validate_input(client_id)
        airline_id = validate_input(airline_id)

        if client_id != -1 and airline_id != -1:
            records_json[type_delete] = [element for element in records_json[type_delete] if
                                         element["Client_ID"] != client_id and
                                         element["Airline_ID"] != airline_id]
        else:

            return client_id # IDs NOT FOUND

    elif type_delete == "Client":
        client_id = validate_input(client_id)

        if client_id != -1:
            records_json[type_delete] = [element for element in records_json[type_delete] if
                                         element["ID"] != client_id]
        else:
            return client_id #ID NOT FOUND

    elif type_delete == "Airline":
        airline_id = validate_input(airline_id)

        if airline_id != -1:
            records_json[type_delete] = [element for element in records_json[type_delete] if
                                         element["ID"] != airline_id]
        else:
            return airline_id #ID NOT FOUND
    else:
        result = -2
        return result # TYPE NOT FOUND

records = {"Client": [], "Airline": [], "Flight": []} 

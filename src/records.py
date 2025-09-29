def create_client_record(id, name, addr1, addr2, addr3, city, state, zip_code, country, phone):
    return {
        'ID': id,
        'Type': 'Client',
        'Name': name,
        'Address Line 1': addr1,
        'Address Line 2': addr2,
        'Address Line 3': addr3,
        'City': city,
        'State': state,
        'Zip Code': zip_code,
        'Country': country,
        'Phone Number': phone
    }

def create_airline_record(id, company_name):
    return {
        'ID': id,
        'Type': 'Airline',
        'Company Name': company_name
    }

def create_flight_record(client_id, airline_id, date, start_city, end_city):
    return {
        'Client_ID': client_id,
        'Airline_ID': airline_id,
        'Date': date,
        'Start City': start_city,
        'End City': end_city
    }

def search_records(records, **kwargs):
    """Search records by fields (e.g., ID=1, Type='Client')."""
    results = []
    for record in records:
        match = True
        for key, value in kwargs.items():
            if record.get(key) != value:
                match = False
                break
        if match:
            results.append(record)
    return results

def create_record(records, new_record, record_type):
    """Add a new record to the list, with type validation."""
    if record_type == 'Client':
        # Assume validation here (e.g., all fields present)
        records.append(new_record)
    elif record_type == 'Airline':
        records.append(new_record)
    elif record_type == 'Flight':
        records.append(new_record)
    else:
        raise ValueError("Invalid record type")
    return records  # Return updated list

def update_record(records, id, updates):
    """Update a record by ID with new field values."""
    for record in records:
        if record.get('ID') == id or record.get('Client_ID') == id:  # Handle Flight IDs
            record.update(updates)
            return records
    print("Record not found for update.")
    return records

def delete_record(records, id):
    """Delete a record by ID."""
    records = [r for r in records if r.get('ID') != id and r.get('Client_ID') != id]
    return records

# Example usage (for local testing)
if __name__ == "__main__":
    records = [
        create_client_record(1, 'John Doe', '123 Main St', '', '', 'New York', 'NY', '10001', 'USA', '123-456-7890'),
        create_airline_record(1, 'FlyHigh Airlines'),
        create_flight_record(1, 1, '2025-10-15T10:00:00', 'New York', 'Los Angeles')
    ]
    print("Initial records:", records)

    # Search example
    print("Search by ID 1:", search_records(records, ID=1))

    # Create example
    new_client = create_client_record(2, 'Jane Doe', '456 Elm St', '', '', 'Los Angeles', 'CA', '90001', 'USA', '987-654-3210')
    records = create_record(records, new_client, 'Client')
    print("After create:", records)

    # Update example
    records = update_record(records, 1, {'Name': 'John Smith'})
    print("After update:", records)

    # Delete example
    records = delete_record(records, 1)
    print("After delete:", records)
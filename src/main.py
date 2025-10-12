   
# src/main.py
# GUI for Record Management System, 
# handles user interface and integrates with records.py


from dataclasses import fields
from posixpath import exists
import tkinter as tk
from tkinter import ttk, messagebox
from records import create_record, delete_record, update_record, search_records, validate_input  # import CRUD functions
from storage import load_records, save_records # import storage functions
from functools import partial
import os

# Load records with the correct file path
FILE_PATH = os.path.join(os.path.dirname(__file__), "data", "test_records.json")
records = load_records(FILE_PATH)

if not isinstance(records, dict):
    # If records is a list, convert to dict with all records as "Client"
    records = {"Client": records, "Airline": [], "Flight": []}
        
def main():
    """Main function to initialize and run the GUI application."""

    def get_fields_for_type(record_type):
        """Return field definitions for a given record type."""
        if record_type == "Client":
            return [
                ("ID (Auto):", tk.Entry, {"state": "disabled"}),
                ("Name:", tk.Entry, {}),
                ("Address Line 1:", tk.Entry, {}),
                ("Address Line 2:", tk.Entry, {}),
                ("Address Line 3:", tk.Entry, {}),
                ("City:", tk.Entry, {}),
                ("State:", tk.Entry, {}),
                ("Zip Code:", tk.Entry, {}),
                ("Country:", tk.Entry, {}),
                ("Phone Number:", tk.Entry, {})
            ]
        elif record_type == "Airline":
                return [
                    ("ID (Auto):", tk.Entry, {"state": "disabled"}),
                    ("Company Name:", tk.Entry, {})
                ]
        elif record_type == "Flight":
            return [
                ("Client_ID:", tk.Entry, {}),
                ("Airline_ID:", tk.Entry, {}),
                ("Date:", tk.Entry, {}),
                ("Start City:", tk.Entry, {}),
                ("End City:", tk.Entry, {})
            ]
        return []
    
    def set_section(section):
        """Set the current section and refresh the treeview."""
        current_section.set(section)
        refresh_treeview()

    # Initialize main window    
    root = tk.Tk()
    root.title("Record Management System - Accessible Interface")
    root.geometry("1200x600")
    root.configure(bg="#333333")

    # Variable to track current section
    current_section = tk.StringVar(value="Client")

    # Create control frame with section selection buttons
    control_frame = tk.Frame(root, bg="#333333")
    control_frame.pack(pady=10)
    tk.Button(control_frame, text="Client", command=lambda: set_section("Client"), font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
    tk.Button(control_frame, text="Airline", command=lambda: set_section("Airline"), font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
    tk.Button(control_frame, text="Flight", command=lambda: set_section("Flight"), font=("Arial", 12)).pack(side=tk.LEFT, padx=5)

    # Create display frame for records
    display_frame = tk.Frame(root, bg="#333333")
    display_frame.pack(pady=10, fill="both", expand=True)
    tk.Label(display_frame, text="Records:", fg="white", bg="#333333").pack()

    def update_treeview_columns():
        """Configure treeview columns based on the current section."""
        record_type = current_section.get()
        if record_type == "Client":
            columns = ("ID", "Name", "Address Line 1","Address Line 2","Zip Code", "Country" "Address Line 3", "City", "Phone Number")
        elif record_type == "Airline":
            columns = ("ID", "Company Name")
        elif record_type == "Flight":
            columns = ("Client_ID/Airline_ID", "Date", "Start City", "End City")
        tree["columns"] = columns
        for col in columns:
            if col == "ID":
                tree.column(col, width=60)
            else:
                tree.column(col, width=120)
            tree.heading(col, text=col)

    def setup_treeview():
        """Initialize the treeview widget for displaying records."""
        global tree
        tree = ttk.Treeview(display_frame, show="headings")
        update_treeview_columns()
        tree.pack(fill="both", expand=True)

    setup_treeview()

    def refresh_treeview():
        """Refresh treeview to display records for the current section."""
        for item in tree.get_children():
            tree.delete(item)
        update_treeview_columns()
        record_type = current_section.get()
        for record in records[record_type]:
            if isinstance(record, dict):
                if record_type == "Airline":
                    values = (
                        record.get("ID", ""),
                        record.get("Company Name", "")
                    )
                elif record_type == "Flight":
                    values = (
                        f"C:{record.get('Client_ID', '')}/A:{record.get('Airline_ID', '')}",
                        record.get("Date", ""),
                        record.get("Start City", ""),
                        record.get("End City", "")
                    )
                else:  # Client
                    values = (
                        record.get("ID", ""),
                        record.get("Name", ""),
                        record.get("Address Line 1", ""),
                        record.get("Address Line 2", ""),
                        record.get("Address Line 3", ""),
                        record.get("City", ""),
                        record.get("State", ""),
                        record.get("Zip Code", ""),
                        record.get("Country", ""),
                        record.get("Phone Number", "")
                    )
                tree.insert("", "end", values=values)

   
    # Create form frame for search functionality
    form_frame = tk.Frame(root, bg="#333333")
    form_frame.pack(pady=10)
    
    tk.Label(form_frame, text="Type:", fg="white", bg="#333333").grid(row=0, column=0, sticky="e", pady=10)
    type_options = ["Client", "Airline",]
    type_var_popup = tk.StringVar(value=type_options[0])
    type_menu = ttk.Combobox(form_frame, textvariable=type_var_popup, values=type_options, state="readonly")
    type_menu.grid(row=0, column=1, padx=5, pady=10)

    tk.Label(form_frame, text="ID:", fg="white", bg="#333333").grid(row=1, column=0, sticky="e", pady=10)
    id_entry = tk.Entry(form_frame)
    id_entry.grid(row=1, column=1, padx=5, pady=10)

    def submit_search():
        """Search for records by ID and display results in treeview."""
        selected_type = type_var_popup.get()
        record_id = id_entry.get().strip()
        if not record_id:
            messagebox.showwarning("Input Error", "ID cannot be blank.")
            return
        if not record_id.isdigit():
            messagebox.showerror("Input Error", "ID must be a number.")
            return

        results = search_records(records, record_id, selected_type)
        print(f"Search results for Client ID {record_id}: {results}") # Debugging output

        if results == -1:
            messagebox.showerror("Invalid ID", "No record found with that ID.")
            return
        elif results == -2:
            messagebox.showerror("Invalid Type", "No such type in the database.")
            return
        
        # Clear current treeview
        for row in tree.get_children():
            tree.delete(row)
       
        if selected_type == "Client":
            # Set columns for client display
            tree["columns"] = ("ID", "Name", "Address Line 1", "Address Line 2", "Address Line 3", "City", "State", "Zip Code", "Country", "Phone Number")
            for col in tree["columns"]:
                tree.column(col, width=60 if col == "ID" else 120)
                tree.heading(col, text=col)
            
            # Insert client records
            for record in results:
                if isinstance(record, dict):
                    values = (
                        record.get("ID", ""),
                        record.get("Name", ""),
                        record.get("Address Line 1", ""),
                        record.get("Address Line 2", ""),
                        record.get("Address Line 3", ""),
                        record.get("City", ""),
                        record.get("State", ""),
                        record.get("Zip Code", ""),
                        record.get("Country", ""),
                        record.get("Phone Number", "")
                    )
                    tree.insert("", "end", values=values)

                    # Find and display associated flights
                    client_id_val = int(record.get("ID", 0))  # Convert to int for comparison
                    flights = [f for f in records["Flight"] if f.get("Client_ID") == client_id_val]
                    if flights:
                        # Temporarily set columns for flight display
                        tree["columns"] = ("Client_ID/Airline_ID", "Date", "Start City", "End City", "Airline Name")
                        for col in tree["columns"]:
                            tree.column(col, width=120)
                            tree.heading(col, text=col)
                        
                        # Insert flight records
                        for flight in flights:
                            airline = next((a for a in records["Airline"] if a.get("ID") == flight.get("Airline_ID")), {})
                            flight_values = (
                                f"C:{flight.get('Client_ID', '')}/A:{flight.get('Airline_ID', '')}",
                                flight.get("Date", ""),
                                flight.get("Start City", ""),
                                flight.get("End City", ""),
                                airline.get("Company Name", "")
                            )
                            tree.insert("", "end", values=flight_values)
                        
                        # Restore client columns
                        tree["columns"] = ("ID", "Name", "Address Line 1", "Address Line 2", "Address Line 3", "City", "State", "Zip Code", "Country", "Phone Number")
                        for col in tree["columns"]:
                            tree.column(col, width=60 if col == "ID" else 120)
                            tree.heading(col, text=col)
                
                
        elif selected_type == "Airline":
            # Set columns for airline display
            tree["columns"] = ("ID", "Company Name")
            for col in tree["columns"]:
                tree.column(col, width=60 if col == "ID" else 120)
                tree.heading(col, text=col)
            
            # Insert airline records
            for record in results:
                if isinstance(record, dict):
                    values = (
                        record.get("ID", ""),
                        record.get("Company Name", "")
                    )
                    tree.insert("", "end", values=values)

                    # Find and display associated clients via flights
                    airline_id_val = int(record.get("ID", 0))
                    flights = [f for f in records["Flight"] if f.get("Airline_ID") == airline_id_val]
                    client_ids = set(f.get("Client_ID") for f in flights)
                    if client_ids:
                        # Temporarily set columns for client display
                        tree["columns"] = ("Client ID", "Name", "Address Line 1", "City", "Phone Number")
                        for col in tree["columns"]:
                            tree.column(col, width=120)
                            tree.heading(col, text=col)
                        
                        # Insert client records
                        for client_id in client_ids:
                            client = next((c for c in records["Client"] if c.get("ID") == client_id), None)
                            if client:
                                client_values = (
                                    f"C:{client.get('ID', '')}",
                                    client.get("Name", ""),
                                    client.get("Address Line 1", ""),
                                    client.get("City", ""),
                                    client.get("Phone Number", "")
                                )
                                tree.insert("", "end", values=client_values)
                        
                        # Restore airline columns
                        tree["columns"] = ("ID", "Company Name")
                        for col in tree["columns"]:
                            tree.column(col, width=60 if col == "ID" else 120)
                            tree.heading(col, text=col)

    tk.Button(form_frame, text="Search", command=submit_search).grid(row=2, column=1, pady=10)

    # Bind keyboard shortcuts for CRUD operations
    root.bind("<Alt-c>", lambda e: create_record_popup())
    root.bind("<Alt-d>", lambda e: delete_record_popup())
    root.bind("<Alt-u>", lambda e: update_record_popup())
    root.bind("<Alt-s>", lambda e: submit_search())

    
    def create_record_popup():
        """Display a pop-up form to create a new record based on the current section."""
        selected_type = current_section.get()  # Use current section instead of dropdown
        create_window = tk.Toplevel(root)
        create_window.title(f"Create {selected_type} Record")
        create_window.geometry("400x400")
        create_window.configure(bg="#333333")

        fields = get_fields_for_type(selected_type)  # Define fields
        entries = {}
        for i, (label_text, widget_class, options) in enumerate(fields):
            tk.Label(create_window, text=label_text, fg="white", bg="#333333").grid(row=i, column=0, sticky="e")
            entry = widget_class(create_window, **options)
            entry.grid(row=i, column=1, padx=5)
            entries[label_text.split(":")[0]] = entry
        
        def submit():
            """Handle form submission for creating a new record."""
            record_data = {key: entry.get() for key, entry in entries.items() if key != "ID (Auto)"}
            # Require all fields for Client
            if selected_type == "Client":
                missing = [key for key, value in record_data.items() if not value]
                if missing:
                    messagebox.showwarning("Input Error", f"All fields are required for Client. Missing: {', '.join(missing)}")
                    return
            # Require Company Name for Airline
            if selected_type == "Airline" and not record_data.get("Company Name"):
                messagebox.showwarning("Input Error", "Company Name is required for Airline.")
                return

            # Require all fields for Flight
            if selected_type == "Flight":
                missing = [key for key, value in record_data.items() if not value]
                if missing:
                    messagebox.showwarning("Input Error", f"All fields are required for Flight. Missing: {', '.join(missing)}")
                    return
            try:
                create_record(records, record_data, selected_type.replace('s', ''))  # Map back
                save_records(records, FILE_PATH)
                messagebox.showinfo("Success", f"{selected_type} record created!")
                refresh_treeview()
                create_window.destroy()
            except Exception as exc:
                messagebox.showerror("Validation Error", str(exc))
                
        tk.Button(create_window, text="Submit", command=submit).grid(
            row=len(fields), column=1, pady=10)
        create_window.transient(root)
        create_window.grab_set()
        root.wait_window(create_window)

    # After tree.pack(fill="both", expand=True)
    refresh_treeview()

    def update_record_popup():
        """Display a pop-up to update a record with selectable fields."""
        update_window = tk.Toplevel(root)
        update_window.title("Update Record")
        update_window.geometry("500x700")
        update_window.configure(bg="#333333")

        # Client ID field
        tk.Label(update_window, text="Client ID (required for Client):", fg="white", bg="#333333").grid(row=0, column=0, sticky="e", pady=10)
        client_id_entry = tk.Entry(update_window)
        client_id_entry.grid(row=0, column=1, padx=5, pady=10)

        # Airline ID field
        tk.Label(update_window, text="Airline ID (required for Airline):", fg="white", bg="#333333").grid(row=1, column=0, sticky="e", pady=10)
        airline_id_entry = tk.Entry(update_window)
        airline_id_entry.grid(row=1, column=1, padx=5, pady=10)

        # Flight tickbox
        flight_var = tk.BooleanVar()
        tk.Checkbutton(update_window, text="Flight (Both IDs required)", variable=flight_var, bg="#333333", fg="white").grid(row=2, column=0, columnspan=2, sticky="w")

        # Instruction label (now below the tickbox)
        tk.Label(update_window, text="Tick fields to update", fg="white", bg="#333333", font=("Arial", 10)).grid(
            row=3, column=0, columnspan=3, sticky="w", pady=(0, 10))
       
        # All updatable fields (from create)
        updatable_fields = [
               "Name",
                "Address Line 1",
                "Address Line 2",
                "Address Line 3",
                "City",
                "State",
                "Zip Code",
                "Country",
                "Phone Number",
                "Company Name",
                "Date",
                "Start City",
                "End City"
            ]

        check_vars = {}
        entries = {}
        checkbuttons = {}

        def toggle_entry(field):
            """Enable or disable entry field based on checkbox state."""
            #print(f"Field: {field}, Checked: {check_vars[field].get()}")  # Debug print
            if check_vars[field].get():
                entries[field].config(state="normal")
            else:
                entries[field].delete(0, tk.END)
                entries[field].config(state="disabled")

        # Build tickboxes and entries for each field
        for i, field in enumerate(updatable_fields):
            check_vars[field] = tk.BooleanVar()
            cb = tk.Checkbutton(
                update_window,
                                variable=check_vars[field],
                bg="#333333",
                fg="white",
                selectcolor="black",  # Color when ticked
                activeforeground="white",
                command=partial(toggle_entry, field)
            )
            cb.grid(row=i+5, column=0, sticky="e", padx=(10, 2))
            checkbuttons[field] = cb
            tk.Label(update_window, text=f"{field}:", fg="white", bg="#333333").grid(row=i+5, column=1, sticky="w")
            entry = tk.Entry(update_window, state="disabled")
            entry.grid(row=i+5, column=2, padx=5)
            entries[field] = entry

    def submit_search():
        """Search for records by ID and display results, including flights for clients."""
        selected_type = type_var_popup.get()
        record_id = id_entry.get().strip()
        if not record_id:
            messagebox.showwarning("Input Error", "ID cannot be blank.")
            return
        if not record_id.isdigit():
            messagebox.showerror("Input Error", "ID must be a number.")
            return

        results = search_records(records, record_id, selected_type)

        if results == -1:
            messagebox.showerror("Invalid ID", "No record found with that ID.")
            return
        elif results == -2:
            messagebox.showerror("Invalid Type", "No such type in the database.")
            return

        # Clear current treeview
        for row in tree.get_children():
            tree.delete(row)

        # Use a unified column set to accommodate both client and flight data
        tree["columns"] = ("ID", "Name/Description", "Address Line 1/Date", "Address Line 2/Start City", "Address Line 3/End City", "City/Airline", "State", "Zip Code", "Country", "Phone Number")
        for col in tree["columns"]:
            tree.column(col, width=60 if col == "ID" else 120)
            tree.heading(col, text=col)

        if selected_type == "Client":
            # Insert client records
            for record in results:
                if isinstance(record, dict):
                    values = (
                        record.get("ID", ""),
                        record.get("Name", ""),
                        record.get("Address Line 1", ""),
                        record.get("Address Line 2", ""),
                        record.get("Address Line 3", ""),
                        record.get("City", ""),
                        record.get("State", ""),
                        record.get("Zip Code", ""),
                        record.get("Country", ""),
                        record.get("Phone Number", "")
                    )
                    tree.insert("", "end", values=values)

                    # Find and display associated flights
                    client_id_val = int(record.get("ID", 0))  # Convert to int for comparison
                    print(f"Searching flights for Client ID {client_id_val}")
                    flights = [f for f in records["Flight"] if f.get("Client_ID") == client_id_val or str(f.get("Client_ID")) == str(client_id_val)]
                    print(f"Flights found: {flights}")
                    try:
                        for flight in flights:
                            airline = next((a for a in records["Airline"] if a.get("ID") == flight.get("Airline_ID")), {})
                            flight_values = (
                                f"F:{flight.get('Client_ID', '')}/{flight.get('Airline_ID', '')}",
                                f"Flight: {flight.get('Client_ID', '')}/{flight.get('Airline_ID', '')}",
                                flight.get("Date", ""),
                                flight.get("Start City", ""),
                                flight.get("End City", ""),
                                airline.get("Company Name", ""),
                                "", "", "", ""  # Pad with empty strings to match column count
                            )
                            tree.insert("", "end", values=flight_values)
                    except Exception as e:
                        print(f"Error inserting flight data: {str(e)}")
                        messagebox.showerror("Display Error", f"Failed to display flights: {str(e)}")
        
        elif selected_type == "Airline":
            # Insert airline records
            for record in results:
                if isinstance(record, dict):
                    values = (
                        record.get("ID", ""),
                        record.get("Company Name", ""),
                        "", "", "", "", "", "", "", ""  # Pad with empty strings
                    )
                    tree.insert("", "end", values=values)

                    # Find and display associated clients via flights
                    airline_id_val = int(record.get("ID", 0))
                    print(f"Searching flights for Airline ID {airline_id_val}")
                    flights = [f for f in records["Flight"] if f.get("Airline_ID") == airline_id_val or str(f.get("Airline_ID")) == str(airline_id_val)]
                    print(f"Flights found: {flights}")
                    client_ids = set(f.get("Client_ID") for f in flights)
                    try:
                        for client_id in client_ids:
                            client = next((c for c in records["Client"] if c.get("ID") == client_id or str(c.get("ID")) == str(client_id)), None)
                            if client:
                                client_values = (
                                    f"C:{client.get('ID', '')}",
                                    client.get("Name", ""),
                                    client.get("Address Line 1", ""),
                                    client.get("Address Line 2", ""),
                                    client.get("Address Line 3", ""),
                                    client.get("City", ""),
                                    client.get("State", ""),
                                    client.get("Zip Code", ""),
                                    client.get("Country", ""),
                                    client.get("Phone Number", "")
                                )
                                tree.insert("", "end", values=client_values)
                    except Exception as e:
                        print(f"Error inserting client data: {str(e)}")
                        messagebox.showerror("Display Error", f"Failed to display clients: {str(e)}")

        
        tk.Button(update_window, text="Update", command=submit_update).grid(row=len(updatable_fields)+6, column=2, pady=20)
        update_window.transient(root)
        update_window.grab_set()
        root.wait_window(update_window)

    def delete_record_popup():
        """Display a pop-up to delete a record by Airline ID, Client ID, or both for Flight."""
        delete_window = tk.Toplevel(root)
        delete_window.title("Delete Record")
        delete_window.geometry("350x200")
        delete_window.configure(bg="#333333")

        # Instruction for Airline ID
        tk.Label(delete_window, text="Enter the ID of the Airline you want to delete:", fg="white", bg="#333333", font=("Arial", 9)).grid(row=0, column=0, columnspan=2, sticky="w", pady=(10, 0))
        tk.Label(delete_window, text="Airline ID:", fg="white", bg="#333333").grid(row=1, column=0, sticky="e", pady=5)
        airline_id_entry = tk.Entry(delete_window)
        airline_id_entry.grid(row=1, column=1, padx=5, pady=5)


        # Instruction for Client ID
        tk.Label(delete_window, text="Enter the ID of the client you want to delete:", fg="white", bg="#333333", font=("Arial", 9)).grid(row=2, column=0, columnspan=2, sticky="w", pady=(10, 0))
        tk.Label(delete_window, text="Client ID:", fg="white", bg="#333333").grid(row=3, column=0, sticky="e", pady=5)
        client_id_entry = tk.Entry(delete_window)
        client_id_entry.grid(row=3, column=1, padx=5, pady=5)

        # Instruction for Flight
        tk.Label(delete_window, text="Tick here if you want to delete the flight:", fg="white", bg="#333333", font=("Arial", 9)).grid(row=4, column=0, columnspan=2, sticky="w", pady=(10, 0))
        flight_var = tk.BooleanVar()
        tk.Checkbutton(delete_window, text="Delete Flight (requires both IDs)", variable=flight_var, bg="#333333", fg="white").grid(row=5, column=0, columnspan=2, sticky="w")

        def submit_delete():
            """Handle deletion of a record based on provided IDs."""
            airline_id = airline_id_entry.get().strip()
            client_id = client_id_entry.get().strip()
            is_flight = flight_var.get()
            
            airline_id_val = int(airline_id) if airline_id.isdigit() else None
            client_id_val = int(client_id) if client_id.isdigit() else None

            # Validation
            if is_flight:
                if not airline_id_val or not client_id_val:
                    messagebox.showwarning("Input Error", "Both Airline ID and Client ID must be entered to delete a Flight.")
                    return
                # Call backend for flight
                delete_record(records, "Flight", client_id=client_id_val, airline_id=airline_id_val)
                msg = f"Flight with Airline ID {airline_id_val} and Client ID {client_id_val} deleted."
            else:
                if not airline_id_val and not client_id_val:
                    messagebox.showwarning("Input Error", "Please enter either Airline ID or Client ID.")
                    return
                if airline_id_val and not client_id_val:
                    # Delete Airline
                    delete_record(records, "Airline", airline_id=airline_id_val)
                    msg = f"Airline with ID {airline_id_val} deleted."
                elif client_id_val and not airline_id_val:
                    # Delete Client
                    delete_record(records, "Client", client_id=client_id_val)
                    msg = f"Client with ID {client_id_val} deleted."
                else:
                    # If both are filled but flight not ticked, ask user to tick flight or clear one
                    messagebox.showwarning("Input Error", "Tick 'Delete Flight' to delete both, or clear one ID.")
                    return

            save_records(records, FILE_PATH)
            messagebox.showinfo("Deleted", msg)
            # Refresh the Treeview to reflect deletion
            refresh_treeview()
            delete_window.destroy()

        tk.Button(delete_window, text="Delete", command=submit_delete).grid(row=5, column=9, pady=12)
        delete_window.transient(root)
        delete_window.grab_set()
        root.wait_window(delete_window)
       
    
        tk.Label(form_frame, text="ID:", fg="white", bg="#333333").grid(row=1, column=0, sticky="e", pady=10)
        id_entry = tk.Entry(form_frame)
        id_entry.grid(row=1, column=1, padx=5, pady=10)
         
    
   
     # CRUD buttons
    crud_frame = tk.Frame(root, bg="#333333")
    crud_frame.pack(pady=5)
    tk.Button(crud_frame, text="Create Record", command=create_record_popup, underline=0, font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
    tk.Button(crud_frame, text="Delete Record", command=delete_record_popup, underline=0, font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
    tk.Button(crud_frame, text="Update Record", command=update_record_popup, underline=0, font=("Arial", 12)).pack(side=tk.LEFT, padx=5)    
    
    root.mainloop()

if __name__ == "__main__":
    main()

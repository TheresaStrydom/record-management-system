
# src/main.py
# GUI for Record Management System, 
# handles user interface and integrates with records.py


from dataclasses import fields
from posixpath import exists
import tkinter as tk
from tkinter import ttk, messagebox
from records import create_record, delete_record, update_record, search_records # import CRUD functions
from storage import load_records, save_records # import storage functions
from functools import partial

FILE_PATH = 'records.json'
records = load_records(FILE_PATH)



def get_fields_for_type(record_type):
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
    
    else:
        return []

def main():
    root = tk.Tk()
    root.title("Record Management System - Accessible Interface")
    root.geometry("600x500")
    root.configure(bg="#333333")  # High contrast for accessibility, made background dark gray to help with visibility

    # Display Area, shows the records in a list format
    display_frame = tk.Frame(root, bg="#333333")
    display_frame.pack(pady=10, fill="both", expand=True)
    tk.Label(display_frame, text="Records:", fg="white", bg="#333333").pack()

    # Define columns for the records
    columns = ("ID", "Type", "Name", "Address Line 1", "City", "Phone Number")
    tree = ttk.Treeview(display_frame, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.pack(fill="both", expand=True)

    # create_record
    def create_record_popup():
        """Display a pop-up form to create a new record based on selected type."""
        """
        Create a new entry in the records_json object.
        Raises ValueError with a specific message if validation fails.
        :param records_json: the nested dict of records
        :param data: dict of data to add
        :param type_create: the type of record to create ("Client", "Airline", "Flight")
        """
            
                
        selected_type = type_var.get()  # Get the selected record type from the dropdown
        create_window = tk.Toplevel(root)  # Create a new window for the form
        create_window.title(f"Create {selected_type} Record")  # Dynamic title
        create_window.geometry("400x400")  # Set pop-up size
        create_window.configure(bg="#333333")  # Match background for consistency

        fields = get_fields_for_type(selected_type)  # Get fields based on type

        entries = {}  # Dictionary to store entry widgets by field name
        for i, (label_text, widget_class, options) in enumerate(fields):
            tk.Label(create_window, text=label_text, fg="white", bg="#333333").grid(
                row=i, column=0, sticky="e")  # Label for each field
            entry = widget_class(create_window, **options)  # Create entry widget
            entry.grid(row=i, column=1, padx=5)  # Position entry
            entries[label_text.split(":")[0]] = entry  # Store for data collection


        
        def submit():
            """
            Handle form submission, collecting data and integrating with backend.
            Show specific validation errors to the user for outstanding feedback.
            """
            global records
            record_data = {key: entry.get() for key, entry in entries.items() if key != "ID (Auto)"}
            try:
                create_record(records, record_data, selected_type)
                save_records(records, FILE_PATH)
                messagebox.showinfo("Success", f"{selected_type} record created!")
                # Clear the Treeview
                for row in tree.get_children():
                    tree.delete(row)
                # Insert records for the selected type
                for record in records[selected_type]:
                    values = (
                        record.get("ID", ""),
                        record.get("Type", ""),
                        record.get("Name", ""),
                        record.get("Address Line 1", ""),
                        record.get("City", ""),
                        record.get("Phone Number", "")
                    )
                    tree.insert("", "end", values=values)
                create_window.destroy()
            except Exception as exc:
                # Show specific validation error message to the user
                messagebox.showerror("Validation Error", str(exc))
        
        
        tk.Button(create_window, text="Submit", command=submit).grid(
            row=len(fields), column=1, pady=10)  # Submit button

        create_window.transient(root)  # Keep pop-up on top of main window
        create_window.grab_set()  # Make pop-up modal
        root.wait_window(create_window)  # Pause until pop-up closes

    def update_record_popup():
        """
        Display a pop-up to update a record.
        Shows all fields from create, plus Client ID, Airline ID, and Flight tickbox.
        Only ticked fields are enabled and passed to backend.
        """
        update_window = tk.Toplevel(root)
        update_window.title("Update Record")
        update_window.geometry("500x700")
        update_window.configure(bg="#333333")

        # Instruction label
        tk.Label(update_window, text="Tick fields to update", fg="white", bg="#333333", font=("Arial", 10)).grid(
            row=0, column=0, columnspan=3, sticky="w", pady=(0, 10))

        # Client ID field
        tk.Label(update_window, text="Client ID (required for Client):", fg="white", bg="#333333").grid(row=1, column=0, sticky="e", pady=10)
        client_id_entry = tk.Entry(update_window)
        client_id_entry.grid(row=1, column=1, padx=5, pady=10)

        # Airline ID field
        tk.Label(update_window, text="Airline ID (required for Airline):", fg="white", bg="#333333").grid(row=2, column=0, sticky="e", pady=10)
        airline_id_entry = tk.Entry(update_window)
        airline_id_entry.grid(row=2, column=1, padx=5, pady=10)

        # Flight tickbox
        flight_var = tk.BooleanVar()
        tk.Checkbutton(update_window, text="Flight (Both IDs required)", variable=flight_var, bg="#333333", fg="white").grid(row=3, column=0, columnspan=2, sticky="w")

        # All updatable fields (from create)
        updatable_fields = [
            "Name", "Address Line 1", "Address Line 2", "Address Line 3",
            "City", "State", "Zip Code", "Country", "Phone Number", "Company Name"
        ]

        check_vars = {}
        entries = {}
        checkbuttons = {}

        def toggle_entry(field):
            """Enable/disable entry based on checkbox."""
            print(f"Field: {field}, Checked: {check_vars[field].get()}")  # Debug print
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

        

        def submit_update():
            """
            Validate and submit the update.
            Only ticked fields and ID(s) are sent to backend.
            """
            client_id = client_id_entry.get().strip()
            airline_id = airline_id_entry.get().strip()
            is_flight = flight_var.get()

            # Build update data
            update_data = {}
            updated_fields = []
            for field, var in check_vars.items():
                if var.get():
                    value = entries[field].get().strip()
                    if not value:
                        messagebox.showwarning("Input Error", f"{field} is ticked but empty.")
                        return
                    update_data[field] = value
                    updated_fields.append(field)

            if not updated_fields:
                messagebox.showwarning("Input Error", "Please tick and fill at least one field to update.")
                return

            # Validation for IDs
            if is_flight:
                if not client_id or not airline_id:
                    messagebox.showwarning("Input Error", "Both Client ID and Airline ID must be filled for Flight update.")
                    return
                record_id = None  # Not used for flight, but backend may expect it
            elif client_id and not airline_id:
                record_id = client_id
            elif airline_id and not client_id:
                record_id = airline_id
            else:
                messagebox.showwarning("Input Error", "Please enter either Client ID or Airline ID for update.")
                return

            try:
                if is_flight:
                    # Pass type_create="Flight" and both IDs
                    update_record(records, "Flight", update_data, client_id, airline_id)
                else:
                    # Determine type based on which ID is filled
                    if client_id and not airline_id:
                        update_record(records, "Client", update_data, client_id, None)
                    elif airline_id and not client_id:
                        update_record(records, "Airline", update_data, None, airline_id)
                save_records(records, FILE_PATH)
                messagebox.showinfo("Success", f"Updated: {', '.join(updated_fields)} successfully.")
                # Refresh Treeview
                for row in tree.get_children():
                    tree.delete(row)
                for record_type in records:
                    for record in records[record_type]:
                        values = (
                            record.get("ID", ""),
                            record.get("Type", ""),
                            record.get("Name", ""),
                            record.get("Address Line 1", ""),
                            record.get("City", ""),
                            record.get("Phone Number", "")
                        )
                        tree.insert("", "end", values=values)
                update_window.destroy()
            except Exception as exc:
                messagebox.showerror("Update Error", str(exc))

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
            airline_id = airline_id_entry.get().strip()
            client_id = client_id_entry.get().strip()
            is_flight = flight_var.get()

            # Validation
            if is_flight:
                if not airline_id or not client_id:
                    messagebox.showwarning("Input Error", "Both Airline ID and Client ID must be entered to delete a Flight.")
                    return
                # Call backend for flight
                delete_record(records, airline_id, client_id, "Flight")
                msg = f"Flight with Airline ID {airline_id} and Client ID {client_id} deleted."
            else:
                if not airline_id and not client_id:
                    messagebox.showwarning("Input Error", "Please enter either Airline ID or Client ID.")
                    return
                if airline_id and not client_id:
                    # Delete Airline
                    delete_record(records, airline_id, None, "Airline")
                    msg = f"Airline with ID {airline_id} deleted."
                elif client_id and not airline_id:
                    # Delete Client
                    delete_record(records, None, client_id, "Client")
                    msg = f"Client with ID {client_id} deleted."
                else:
                    # If both are filled but flight not ticked, ask user to tick flight or clear one
                    messagebox.showwarning("Input Error", "Tick 'Delete Flight' to delete both, or clear one ID.")
                    return

            save_records(records, FILE_PATH)
            messagebox.showinfo("Deleted", msg)
            # Refresh the Treeview to reflect deletion
            for row in tree.get_children():
                tree.delete(row)
            for record_type in records:
                for record in records[record_type]:
                    values = (
                        record.get("ID", ""),
                        record.get("Type", ""),
                        record.get("Name", ""),
                        record.get("Address Line 1", ""),
                        record.get("City", ""),
                        record.get("Phone Number", "")
                    )
                    tree.insert("", "end", values=values)
            delete_window.destroy()

        tk.Button(delete_window, text="Delete", command=submit_delete).grid(row=5, column=9, pady=12)
        delete_window.transient(root)
        delete_window.grab_set()
        root.wait_window(delete_window)
       
    def search_record_popup():
        """
        Display a pop-up to search records by ID and type (Client or Airline).
        """
        search_window = tk.Toplevel(root)
        search_window.title("Search Record")
        search_window.geometry("350x180")
        search_window.configure(bg="#333333")

        # Type dropdown
        tk.Label(search_window, text="Type:", fg="white", bg="#333333").grid(row=0, column=0, sticky="e", pady=10)
        type_options = ["Client", "Airline"]
        type_var_popup = tk.StringVar(value=type_options[0])
        type_menu = ttk.Combobox(search_window, textvariable=type_var_popup, values=type_options, state="readonly")
        type_menu.grid(row=0, column=1, padx=5, pady=10)

        # ID entry
        tk.Label(search_window, text="ID:", fg="white", bg="#333333").grid(row=1, column=0, sticky="e", pady=10)
        id_entry = tk.Entry(search_window)
        id_entry.grid(row=1, column=1, padx=5, pady=10)

        def submit_search():
            """
            Search for a record by type and ID, and update the main Treeview.
            Handles special return values for invalid ID or type.
            """
            selected_type = type_var_popup.get()
            record_id = id_entry.get().strip()
            if not record_id:
                messagebox.showwarning("Input Error", "ID cannot be blank.")
                return
            # Call your backend search function
            results = search_records(records, record_id, selected_type)
            if results == -1:
                messagebox.showerror("Invalid ID", "No record found with that ID.")
                return
            elif results == -2:
                messagebox.showerror("Invalid Type", "No such airline in the database.")
                return
            # Otherwise, display results
            for row in tree.get_children():
                tree.delete(row)
            for record in results:
                values = (
                    record.get("ID", ""),
                    record.get("Type", ""),
                    record.get("Name", ""),
                    record.get("Address Line 1", ""),
                    record.get("City", ""),
                    record.get("Phone Number", "")
                )
                tree.insert("", "end", values=values)
            search_window.destroy()
   
        def clear_search():
            """
            Clear the ID entry and reset the Treeview to show all records of the selected type.
            """
            id_entry.delete(0, tk.END)
            selected_type = type_var_popup.get()
            # Reset Treeview to show all records of selected_type
            for row in tree.get_children():
                tree.delete(row)
            for record in records[selected_type]:
                values = (
                    record.get("ID", ""),
                    record.get("Type", ""),
                    record.get("Name", ""),
                    record.get("Address Line 1", ""),
                    record.get("City", ""),
                    record.get("Phone Number", "")
                )
                tree.insert("", "end", values=values)

        # Add search and clear buttons
        tk.Button(search_window, text="Search", command=submit_search).grid(row=2, column=1, pady=10)
        tk.Button(search_window, text="Clear Search", command=clear_search).grid(row=2, column=0, pady=10, sticky="w")
        
        search_window.transient(root)
        search_window.grab_set()
        root.wait_window(search_window)

    # Control Panel section at the top of the window for CRUD operations
    control_frame = tk.Frame(root, bg="#333333")
    control_frame.pack(pady=10)
    tk.Button(control_frame, text="Create Record", command=create_record_popup,
              underline=0, font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
    tk.Button(control_frame, text="Delete Record", command=delete_record_popup,
              underline=0, font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
    tk.Button(control_frame, text="Update Record", command=update_record_popup,
              underline=0, font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
    tk.Button(control_frame, text="Search Record", command=search_record_popup,
              underline=0, font=("Arial", 12)).pack(side=tk.LEFT, padx=5)

    # Keyboard shortcuts for accessibility
    root.bind("<Alt-c>", lambda e: create_record_popup())
    root.bind("<Alt-d>", lambda e: delete_record_popup())
    root.bind("<Alt-u>", lambda e: update_record_popup())
    root.bind("<Alt-s>", lambda e: search_record_popup())

    # Form Section to input record details
    form_frame = tk.Frame(root, bg="#333333")
    form_frame.pack(pady=10)
    tk.Label(form_frame, text="Select Record Type:", fg="white", bg="#333333").grid(row=0, column=0, sticky="e")
    types = ["Client", "Airline"]
    type_var = tk.StringVar(value=types[0])  # Default to Client
    ttk.Combobox(form_frame, textvariable=type_var, values=types, state="readonly").grid(row=0, column=1, padx=5)
    tk.Label(form_frame, text="Name:", fg="white", bg="#333333").grid(row=1, column=0, sticky="e")
    tk.Entry(form_frame).grid(row=1, column=1, padx=5)



        # Set initial focus to the main window, supporting motor-impaired users
    root.focus_set()
    form_frame.focus_set()

    root.mainloop()

if __name__ == "__main__":
    main()
    
    
    
    

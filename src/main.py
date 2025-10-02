
# src/main.py
# GUI for Record Management System, 
# handles user interface and integrates with records.py


from dataclasses import fields
import tkinter as tk
from tkinter import ttk, messagebox
from records import create_record, delete_record, update_record, search_records # import CRUD functions
from storage import load_records, save_records # import storage functions

FILE_PATH = 'src/records.json'
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

        
            """Handle form submission, collecting data with backend integration."""
        def submit():
            global records
            record_data = {key: entry.get() for key, entry in entries.items() if key != "ID (Auto)"}
            create_record(records, record_data, selected_type)
            save_records(records, FILE_PATH)
            messagebox.showinfo("Success", f"{selected_type} record created!")
            # Clear the Treeview
            for row in tree.get_children():
             tree.delete(row)
            # Insert records
            for record in records["Client"]:  # or whichever type you want to display
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

        tk.Button(create_window, text="Submit", command=submit).grid(
            row=len(fields), column=1, pady=10) # Submit button
        
        create_window.transient(root)  # Keep pop-up on top of main window
        create_window.grab_set()  # Make pop-up modal
        root.wait_window(create_window)  # Pause until pop-up closes

    def update_record_popup():
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("No selection", "Please select a record to update.")
            return
        selected_values = tree.item(selected_item, "values")
        selected_type = selected_values[1]  # Assuming "Type" is the second column

        update_window = tk.Toplevel(root)
        update_window.title("Update Record")
        update_window.geometry("400x400")
        update_window.configure(bg="#333333")

        fields = get_fields_for_type(selected_type)
        entries = {}
        for i, (label_text, widget_class, options) in enumerate(fields):
            tk.Label(update_window, text=label_text, fg="white", bg="#333333").grid(
                row=i, column=0, sticky="e")
            entry = widget_class(update_window)
            entry.grid(row=i, column=1, padx=5)
            # Pre-fill with existing value if available
            col_name = label_text.split(":")[0]
            if col_name in tree["columns"]:
                col_index = tree["columns"].index(col_name)
                entry.insert(0, selected_values[col_index])
            entries[col_name] = entry

        def submit_update():
            global records
            updated_data = {key: entry.get() for key, entry in entries.items() if key != "ID (Auto)"}
            record_id = selected_values[0]  # Assuming "ID" is the first column
            update_record(records, int(record_id), updated_data)
            save_records(records, FILE_PATH)
            messagebox.showinfo("Success", "Record updated!")
            update_window.destroy()

        tk.Button(update_window, text="Update", command=submit_update).grid(
            row=len(fields), column=1, pady=10)
        update_window.transient(root)
        update_window.grab_set()
        root.wait_window(update_window)     

    def delete_record_popup():
        """Display a pop-up to delete a record by ID """
        delete_window = tk.Toplevel(root)
        delete_window.title("Delete Record")
        delete_window.geometry("300x150")
        delete_window.configure(bg="#333333")
        tk.Label(delete_window, text="ID:", fg="white", bg="#333333").grid(row=0, column=0, sticky="e")
        id_entry = tk.Entry(delete_window)
        id_entry.grid(row=0, column=1, padx=5)
        tk.Button(delete_window, text="Delete", command=lambda: print("Delete TBD")).grid(row=1, column=1, pady=10)
        delete_window.transient(root)
        delete_window.grab_set()
        root.wait_window(delete_window)
       
    def search_record_popup():
        selected_type = type_var.get()
        search_window = tk.Toplevel(root)
        search_window.title(f"Search {selected_type} Record")
        search_window.geometry("400x400")
        search_window.configure(bg="#333333")

        fields = get_fields_for_type(selected_type)  # Reuse the same helper
        entries = {}
        for i, (label_text, widget_class, options) in enumerate(fields):
            tk.Label(search_window, text=label_text, fg="white", bg="#333333").grid(
                row=i, column=0, sticky="e")
            entry = widget_class(search_window)  # For search, don't use options like "disabled"
            entry.grid(row=i, column=1, padx=5)
            entries[label_text.split(":")[0]] = entry

        def submit_search():
             # Collect only non-empty fields for search
            criteria = {key: entry.get() for key, entry in entries.items() if entry.get()}
            results = search_records(records, selected_type, criteria)  # <-- Call your backend search
            # Optionally, update the Treeview with the results:
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

        tk.Button(search_window, text="Search", command=submit_search).grid(
            row=len(fields), column=1, pady=10)
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
    
    
    
    

import tkinter as tk
from tkinter import ttk, messagebox
''' from src.records import create_record, delete_record, update_record, search_records # Placeholder until merged
from src.storage import load_records, save_records # Placeholder until merged
'''
FILE_PATH = 'src/record/record.json'

def main():
    root = tk.Tk()
    root.title("Record Management System - Accessible Interface")
    root.geometry("600x500")
    root.configure(bg="#333333")  # High contrast for accessibility, made background dark gray to help with visibility

    # Placeholder functions, to be integrated to code later
    # Placeholder functions to be replaced with backend calls after PR merge
    def create_placeholder():
        """Display a pop-up form to create a new record based on selected type."""
        selected_type = type_var.get()  # Get the selected record type from the dropdown
        create_window = tk.Toplevel(root)  # Create a new window for the form
        create_window.title(f"Create {selected_type} Record")  # Dynamic title
        create_window.geometry("400x400")  # Set pop-up size
        create_window.configure(bg="#333333")  # Match background for consistency

        fields = []  # List to hold field definitions for the selected record type
        if selected_type == "Client":
            fields = [
                ("ID (Auto):", tk.Entry, {"state": "disabled"}),  # Read-only ID field
                ("Name:", tk.Entry, {}),  # User input for name
                ("Address Line 1:", tk.Entry, {}),  # Address fields
                ("Address Line 2:", tk.Entry, {}),
                ("Address Line 3:", tk.Entry, {}),
                ("City:", tk.Entry, {}),
                ("State:", tk.Entry, {}),
                ("Zip Code:", tk.Entry, {}),
                ("Country:", tk.Entry, {}),
                ("Phone Number:", tk.Entry, {})
            ]
        elif selected_type == "Airline":
            fields = [("ID (Auto):", tk.Entry, {"state": "disabled"}), ("Company Name:", tk.Entry, {})]
        elif selected_type == "Flight":
            fields = [
                ("Client ID:", tk.Entry, {}),
                ("Airline ID:", tk.Entry, {}),
                ("Date:", tk.Entry, {}),  # Placeholder, plan to use DateEntry later
                ("Start City:", tk.Entry, {}),
                ("End City:", tk.Entry, {})
            ]

        entries = {}  # Dictionary to store entry widgets by field name
        for i, (label_text, widget_class, options) in enumerate(fields):
            tk.Label(create_window, text=label_text, fg="white", bg="#333333").grid(
                row=i, column=0, sticky="e")  # Label for each field
            entry = widget_class(create_window, **options)  # Create entry widget
            entry.grid(row=i, column=1, padx=5)  # Position entry
            entries[label_text.split(":")[0]] = entry  # Store for data collection

        def submit():
            """Handle form submission, collecting data for future backend integration."""
            record_data = {key: entry.get() for key, entry in entries.items() if key != "ID (Auto)"}
            print(f"Submit {selected_type} data: {record_data}")  # Temporary output
            create_window.destroy()  # Close the pop-up

        tk.Button(create_window, text="Submit", command=submit).grid(
            row=len(fields), column=1, pady=10)  # Submit button
        create_window.transient(root)  # Keep pop-up on top of main window
        create_window.grab_set()  # Make pop-up modal
        root.wait_window(create_window)  # Pause until pop-up closes

    def update_placeholder():
        """Display a pop-up to update an existing record (placeholder for backend integration)."""
        update_window = tk.Toplevel(root)
        update_window.title("Update Record")
        update_window.geometry("300x150")
        update_window.configure(bg="#333333")
        tk.Label(update_window, text="ID:", fg="white", bg="#333333").grid(row=0, column=0, sticky="e")
        id_entry = tk.Entry(update_window)
        id_entry.grid(row=0, column=1, padx=5)
        tk.Button(update_window, text="Submit", command=lambda: print("Update TBD")).grid(row=1, column=1, pady=10)
        update_window.transient(root)
        update_window.grab_set()
        root.wait_window(update_window)
        # TODO: Integrate with update_record after PR merge

    def delete_placeholder():
        """Display a pop-up to delete a record by ID (placeholder for backend integration)."""
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
        # TODO: Integrate with delete_record after PR merge

    def search_placeholder():
        """Display a pop-up to search records by ID or type (placeholder for backend integration)."""
        search_window = tk.Toplevel(root)
        search_window.title("Search Record")
        search_window.geometry("300x200")
        search_window.configure(bg="#333333")
        tk.Label(search_window, text="ID (optional):", fg="white", bg="#333333").grid(row=0, column=0, sticky="e")
        id_entry = tk.Entry(search_window)
        id_entry.grid(row=0, column=1, padx=5)
        tk.Label(search_window, text="Type (optional):", fg="white", bg="#333333").grid(row=1, column=0, sticky="e")
        type_var_search = tk.StringVar()
        ttk.Combobox(search_window, textvariable=type_var_search, values=["", "Client", "Airline", "Flight"]).grid(row=1, column=1, padx=5)
        tk.Button(search_window, text="Search", command=lambda: print("Search TBD")).grid(row=2, column=1, pady=10)
        search_window.transient(root)
        search_window.grab_set()
        root.wait_window(search_window)
        # TODO: Integrate with search_records after PR merge

    # Control Panel section at the top of the window for CRUD operations
    control_frame = tk.Frame(root, bg="#333333")
    control_frame.pack(pady=10)
    tk.Button(control_frame, text="Create Record", command=create_placeholder,
              underline=0, font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
    tk.Button(control_frame, text="Delete Record", command=delete_placeholder,
              underline=0, font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
    tk.Button(control_frame, text="Update Record", command=update_placeholder,
              underline=0, font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
    tk.Button(control_frame, text="Search Record", command=search_placeholder,
              underline=0, font=("Arial", 12)).pack(side=tk.LEFT, padx=5)

    # Keyboard shortcuts for accessibility
    root.bind("<Alt-c>", lambda e: create_placeholder())
    root.bind("<Alt-d>", lambda e: delete_placeholder())
    root.bind("<Alt-u>", lambda e: update_placeholder())
    root.bind("<Alt-s>", lambda e: search_placeholder())

    # Form Section to input record details
    form_frame = tk.Frame(root, bg="#333333")
    form_frame.pack(pady=10)
    tk.Label(form_frame, text="Select Record Type:", fg="white", bg="#333333").grid(row=0, column=0, sticky="e")
    types = ["Client", "Airline", "Flight"]
    type_var = tk.StringVar(value=types[0])  # Default to Client
    ttk.Combobox(form_frame, textvariable=type_var, values=types, state="readonly").grid(row=0, column=1, padx=5)
    tk.Label(form_frame, text="Name:", fg="white", bg="#333333").grid(row=1, column=0, sticky="e")
    tk.Entry(form_frame).grid(row=1, column=1, padx=5)

    # Display Area, shows the records in a list format
    display_frame = tk.Frame(root, bg="#333333")
    display_frame.pack(pady=10, fill="both", expand=True)
    tk.Label(display_frame, text="Records:", fg="white", bg="#333333").pack()
    tree = ttk.Treeview(display_frame, columns=("ID", "Type", "Name", "Address Line 1", "City", "Phone Number"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col.replace("_", " ").title())  # Set column headers
    tree.insert("", "end", values=("1", "Client", "John Doe", "123 St", "London", "123-456-7890"))  # Placeholder data
    tree.pack(fill="both", expand=True)
    scrollbar = ttk.Scrollbar(display_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill="y")

    # Set initial focus to the main window, supporting motor-impaired users
    root.focus_set()
    form_frame.focus_set()

    root.mainloop()

if __name__ == "__main__":
    main()
    
    
    
    
    def search_placeholder(): print("Search button clicked - TBD")

    # Control Panel section at the top of the window for CRUD operations
    control_frame = tk.Frame(root, bg="#333333")
    control_frame.pack(pady=10)
    tk.Button(control_frame, text="Create Record", command=create_placeholder,
              underline=0, font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
    tk.Button(control_frame, text="Delete Record", command=delete_placeholder,
              underline=0, font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
    tk.Button(control_frame, text="Update Record", command=update_placeholder,
              underline=0, font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
    tk.Button(control_frame, text="Search Record", command=search_placeholder,
              underline=0, font=("Arial", 12)).pack(side=tk.LEFT, padx=5)

    # Keyboard shortcuts for accessibility
    root.bind("<Alt-c>", lambda e: create_placeholder())
    root.bind("<Alt-d>", lambda e: delete_placeholder())
    root.bind("<Alt-u>", lambda e: update_placeholder())
    root.bind("<Alt-s>", lambda e: search_placeholder())

    # Form Section to input record details
    form_frame = tk.Frame(root, bg="#333333")
    form_frame.pack(pady=10)
    tk.Label(form_frame, text="Select Record Type:", fg="white", bg="#333333").grid(row=0, column=0, sticky="e")
    types = ["Client", "Airline", "Flight"]
    type_var = tk.StringVar(value=types[0])
    ttk.Combobox(form_frame, textvariable=type_var, values=types, state="readonly").grid(row=0, column=1, padx=5)
    tk.Label(form_frame, text="Name:", fg="white", bg="#333333").grid(row=1, column=0, sticky="e")
    tk.Entry(form_frame).grid(row=1, column=1, padx=5)

    # Display Area, shows the records in a list format
    display_frame = tk.Frame(root, bg="#333333")
    display_frame.pack(pady=10, fill="both", expand=True)
    tk.Label(display_frame, text="Records:", fg="white", bg="#333333").pack()
    tree = ttk.Treeview(display_frame, columns=("ID", "Type", "Name", "Address Line 1", "City", "Phone Number"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col.replace("_", " ").title())
    tree.insert("", "end", values=("1", "Client", "John Doe", "123 St", "London", "123-456-7890"))
    tree.pack(fill="both", expand=True)
    scrollbar = ttk.Scrollbar(display_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill="y")

    # Set initial focus to the main window, supporting motor-impaired users who rely on the Tab key to move between fields
    root.focus_set()
    form_frame.focus_set()

    root.mainloop()

if __name__ == "__main__":
    main()
    
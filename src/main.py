import tkinter as tk
from tkinter import ttk


def main():
    root = tk.Tk()
    root.title("Record Management System - Accessible Interface")
    root.geometry("600x500")
    root.configure(bg="#333333")  # High contrast for accessibility, made background dark gray to help with visibility

    # Placeholder functions, to be integrated to code later
    def create_placeholder(): 
        selected_type = type_var.get()
        create_window = tk.Toplevel(root)
        create_window.title(f"Create {selected_type} Record")
        create_window.geometry("400x400")
        create_window.configure(bg="#333333")
        
        # Dynamic fields based on type
        fields = []
        if selected_type == "Client":
            fields = [
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
        elif selected_type == "Airline":
            fields = [
                ("ID (Auto):", tk.Entry, {"state": "disabled"}),
                ("Company Name:", tk.Entry, {})
            ]
        elif selected_type == "Flight":
            fields = [
                ("Client ID:", tk.Entry, {}),
                ("Airline ID:", tk.Entry, {}),
                ("Date:", tk.Entry, {}),  # Placeholder, use DateEntry later
                ("Start City:", tk.Entry, {}),
                ("End City:", tk.Entry, {})
            ]

        for i, (label_text, widget_class, options) in enumerate(fields):
            tk.Label(create_window, text=label_text, fg="white", bg="#333333").grid(row=i, column=0, sticky="e")
            tk.Entry(create_window, **options).grid(row=i, column=1, padx=5)
        tk.Button(create_window, text="Submit", command=lambda: print(f"Submit {selected_type} - TBD")).grid(row=len(fields), column=1, pady=10)

        create_window.transient(root)
        create_window.grab_set()
        root.wait_window(create_window)
        
        
    def delete_placeholder(): print("Delete button clicked - TBD")
    def update_placeholder(): print("Update button clicked - TBD")
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
    
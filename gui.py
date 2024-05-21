import tkinter as tk
from tkinter import messagebox, ttk
from customer import Customer
from database import Database

class CustomerGUI:
    def __init__(self):
        self.db = Database()
        self.db.connect()

        self.root = tk.Tk()
        self.root.title("Vinmart Customer Management")
        self.root.geometry("600x400")
        self.root.configure(bg='#f0f0f0')

        self.create_widgets()

    def create_widgets(self):
        # Title
        title = tk.Label(self.root, text="Vinmart Customer Management", font=("Helvetica", 16, "bold"), bg='#f0f0f0')
        title.grid(row=0, columnspan=2, pady=10)

        # Name
        lbl_name = tk.Label(self.root, text="Name:", bg='#f0f0f0')
        lbl_name.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        self.entry_name = tk.Entry(self.root, width=30)
        self.entry_name.grid(row=1, column=1, padx=10, pady=5)

        # Phone
        lbl_phone = tk.Label(self.root, text="Phone:", bg='#f0f0f0')
        lbl_phone.grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
        self.entry_phone = tk.Entry(self.root, width=30)
        self.entry_phone.grid(row=2, column=1, padx=10, pady=5)

        # Address
        lbl_address = tk.Label(self.root, text="Address:", bg='#f0f0f0')
        lbl_address.grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)
        self.entry_address = tk.Entry(self.root, width=30)
        self.entry_address.grid(row=3, column=1, padx=10, pady=5)

        # Email
        lbl_email = tk.Label(self.root, text="Email:", bg='#f0f0f0')
        lbl_email.grid(row=4, column=0, padx=10, pady=5, sticky=tk.E)
        self.entry_email = tk.Entry(self.root, width=30)
        self.entry_email.grid(row=4, column=1, padx=10, pady=5)

        # Buttons
        btn_frame = tk.Frame(self.root, bg='#f0f0f0')
        btn_frame.grid(row=5, columnspan=2, pady=10)

        self.button_add = tk.Button(btn_frame, text="Add Customer", command=self.add_customer, width=15, bg='#4CAF50', fg='white')
        self.button_add.grid(row=0, column=0, padx=5)

        self.button_update = tk.Button(btn_frame, text="Update Customer", command=self.update_customer, width=15, bg='#2196F3', fg='white')
        self.button_update.grid(row=0, column=1, padx=5)

        self.button_delete = tk.Button(btn_frame, text="Delete Customer", command=self.delete_customer, width=15, bg='#F44336', fg='white')
        self.button_delete.grid(row=0, column=2, padx=5)

        self.button_search = tk.Button(btn_frame, text="Search Customer", command=self.search_customer, width=15, bg='#FF9800', fg='white')
        self.button_search.grid(row=1, column=0, padx=5, pady=5)

        self.button_display = tk.Button(btn_frame, text="Display All Customers", command=self.display_customers, width=15, bg='#9C27B0', fg='white')
        self.button_display.grid(row=1, column=1, padx=5, pady=5)

        # Treeview for displaying customers
        self.tree = ttk.Treeview(self.root, columns=("ID", "Name", "Phone", "Address", "Email"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Phone", text="Phone")
        self.tree.heading("Address", text="Address")
        self.tree.heading("Email", text="Email")

        self.tree.column("ID", width=30)
        self.tree.column("Name", width=100)
        self.tree.column("Phone", width=100)
        self.tree.column("Address", width=150)
        self.tree.column("Email", width=150)

        self.tree.grid(row=6, columnspan=2, pady=10, padx=10)

    def add_customer(self):
        name = self.entry_name.get()
        phone = self.entry_phone.get()
        address = self.entry_address.get()
        email = self.entry_email.get()

        customer = Customer(None, name, phone, address, email)
        query = "INSERT INTO customers (name, phone, address, email) VALUES (%s, %s, %s, %s)"
        self.db.execute_query(query, (name, phone, address, email))
        messagebox.showinfo("Info", "Customer added successfully")
        self.display_customers()

    def update_customer(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a customer to update")
            return

        customer_id = self.tree.item(selected_item, 'values')[0]
        name = self.entry_name.get()
        phone = self.entry_phone.get()
        address = self.entry_address.get()
        email = self.entry_email.get()

        query = "UPDATE customers SET name=%s, phone=%s, address=%s, email=%s WHERE customer_id=%s"
        self.db.execute_query(query, (name, phone, address, email, customer_id))
        messagebox.showinfo("Info", "Customer updated successfully")
        self.display_customers()

    def delete_customer(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a customer to delete")
            return

        customer_id = self.tree.item(selected_item, 'values')[0]
        query = "DELETE FROM customers WHERE customer_id=%s"
        self.db.execute_query(query, (customer_id,))
        messagebox.showinfo("Info", "Customer deleted successfully")
        self.display_customers()

    def search_customer(self):
        search_name = self.entry_name.get()
        query = "SELECT * FROM customers WHERE name LIKE %s"
        results = self.db.fetch_results(query, ('%' + search_name + '%',))
        self.update_treeview(results)

    def display_customers(self):
        query = "SELECT * FROM customers"
        results = self.db.fetch_results(query)
        self.update_treeview(results)

    def update_treeview(self, results):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in results:
            self.tree.insert("", "end", values=row)

    def run(self):
        self.root.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import re


EMAIL_PATTERN = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)


class ContactManager:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Contact Manager"
        )

        self.root.geometry(
            "900x600"
        )

        # MySQL connection
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="contacts_db"
        )

        self.cursor = (
            self.connection.cursor()
        )

        self.create_table()

        self.create_gui()

        self.load_contacts()


    def create_table(self):

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Contact (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(150) UNIQUE,
                phone VARCHAR(30),
                category VARCHAR(30),
                notes TEXT
            )
        """)

        self.connection.commit()


    def create_gui(self):

        # ---------- Form ----------
        form = tk.Frame(
            self.root
        )

        form.pack(
            pady=10
        )

        self.entries = {}

        fields = [
            "Name",
            "Email",
            "Phone",
            "Category"
        ]

        for row, field in enumerate(fields):

            tk.Label(
                form,
                text=field
            ).grid(
                row=row,
                column=0,
                padx=5,
                pady=5
            )

            entry = tk.Entry(
                form,
                width=35
            )

            entry.grid(
                row=row,
                column=1,
                padx=5,
                pady=5
            )

            self.entries[field] = entry


        # Notes using Text widget
        tk.Label(
            form,
            text="Notes"
        ).grid(
            row=4,
            column=0
        )

        self.notes = tk.Text(
            form,
            width=35,
            height=4
        )

        self.notes.grid(
            row=4,
            column=1
        )


        # Category Combobox
        self.entries["Category"].destroy()

        self.category = ttk.Combobox(
            form,
            values=[
                "Faculty",
                "Student",
                "Friend",
                "Family",
                "Other"
            ],
            state="readonly",
            width=32
        )

        self.category.grid(
            row=3,
            column=1
        )


        # Buttons
        tk.Button(
            form,
            text="Add",
            command=self.add_contact
        ).grid(
            row=5,
            column=0,
            pady=10
        )

        tk.Button(
            form,
            text="Update",
            command=self.update_contact
        ).grid(
            row=5,
            column=1
        )

        tk.Button(
            form,
            text="Delete",
            command=self.delete_contact
        ).grid(
            row=5,
            column=2
        )


        # ---------- Search ----------
        search_frame = tk.Frame(
            self.root
        )

        search_frame.pack(
            pady=5
        )

        tk.Label(
            search_frame,
            text="Search:"
        ).pack(
            side=tk.LEFT
        )

        self.search_entry = tk.Entry(
            search_frame,
            width=30
        )

        self.search_entry.pack(
            side=tk.LEFT,
            padx=5
        )

        self.search_type = ttk.Combobox(
            search_frame,
            values=[
                "name",
                "email",
                "phone"
            ],
            state="readonly",
            width=10
        )

        self.search_type.set(
            "name"
        )

        self.search_type.pack(
            side=tk.LEFT
        )

        tk.Button(
            search_frame,
            text="Search",
            command=self.search_contacts
        ).pack(
            side=tk.LEFT,
            padx=5
        )


        # ---------- Contact List ----------
        columns = (
            "id",
            "name",
            "email",
            "phone",
            "category",
            "notes"
        )

        self.tree = ttk.Treeview(
            self.root,
            columns=columns,
            show="headings"
        )

        for column in columns:

            self.tree.heading(
                column,
                text=column.title()
            )

            self.tree.column(
                column,
                width=130
            )

        self.tree.pack(
            fill=tk.BOTH,
            expand=True,
            padx=10,
            pady=10
        )

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.select_contact
        )


    def get_values(self):

        return {
            "name":
                self.entries["Name"].get().strip(),

            "email":
                self.entries["Email"].get().strip(),

            "phone":
                self.entries["Phone"].get().strip(),

            "category":
                self.category.get().strip(),

            "notes":
                self.notes.get(
                    "1.0",
                    tk.END
                ).strip()
        }


    def validate(self, data):

        if not data["name"]:

            return "Name is required."

        if not EMAIL_PATTERN.match(
            data["email"]
        ):

            return "Invalid email address."

        return None


    def add_contact(self):

        data = self.get_values()

        error = self.validate(data)

        if error:

            messagebox.showerror(
                "Validation Error",
                error
            )

            return

        try:

            self.cursor.execute("""
                INSERT INTO Contact
                (name,email,phone,category,notes)
                VALUES (%s,%s,%s,%s,%s)
            """, (
                data["name"],
                data["email"],
                data["phone"],
                data["category"],
                data["notes"]
            ))

            self.connection.commit()

            self.load_contacts()

            messagebox.showinfo(
                "Success",
                "Contact inserted."
            )

        except mysql.connector.Error as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )


    def get_selected_id(self):

        selected = self.tree.selection()

        if not selected:
            return None

        values = self.tree.item(
            selected[0]
        )["values"]

        return values[0]


    def update_contact(self):

        contact_id = (
            self.get_selected_id()
        )

        if contact_id is None:

            messagebox.showwarning(
                "Warning",
                "Select a contact."
            )

            return

        data = self.get_values()

        error = self.validate(data)

        if error:

            messagebox.showerror(
                "Validation Error",
                error
            )

            return

        try:

            self.cursor.execute("""
                UPDATE Contact
                SET name=%s,
                    email=%s,
                    phone=%s,
                    category=%s,
                    notes=%s
                WHERE id=%s
            """, (
                data["name"],
                data["email"],
                data["phone"],
                data["category"],
                data["notes"],
                contact_id
            ))

            self.connection.commit()

            self.load_contacts()

        except mysql.connector.Error as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )


    def delete_contact(self):

        contact_id = (
            self.get_selected_id()
        )

        if contact_id is None:
            return

        self.cursor.execute(
            "DELETE FROM Contact WHERE id=%s",
            (contact_id,)
        )

        self.connection.commit()

        self.load_contacts()


    def load_contacts(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        self.cursor.execute("""
            SELECT id,name,email,phone,category,notes
            FROM Contact
            ORDER BY name
        """)

        for row in self.cursor.fetchall():

            self.tree.insert(
                "",
                tk.END,
                values=row
            )


    def search_contacts(self):

        keyword = (
            self.search_entry
            .get()
            .strip()
        )

        search_type = (
            self.search_type.get()
        )

        if search_type not in [
            "name",
            "email",
            "phone"
        ]:
            return

        query = f"""
            SELECT id,name,email,phone,category,notes
            FROM Contact
            WHERE {search_type} LIKE %s
            ORDER BY name
        """

        self.cursor.execute(
            query,
            ("%" + keyword + "%",)
        )

        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in self.cursor.fetchall():

            self.tree.insert(
                "",
                tk.END,
                values=row
            )


    def select_contact(self, event):

        selected = (
            self.tree.selection()
        )

        if not selected:
            return

        values = self.tree.item(
            selected[0]
        )["values"]

        self.entries["Name"].delete(
            0,
            tk.END
        )

        self.entries["Name"].insert(
            0,
            values[1]
        )

        self.entries["Email"].delete(
            0,
            tk.END
        )

        self.entries["Email"].insert(
            0,
            values[2]
        )

        self.entries["Phone"].delete(
            0,
            tk.END
        )

        self.entries["Phone"].insert(
            0,
            values[3]
        )

        self.category.set(
            values[4]
        )

        self.notes.delete(
            "1.0",
            tk.END
        )

        self.notes.insert(
            "1.0",
            values[5]
        )


root = tk.Tk()

app = ContactManager(root)

root.mainloop()
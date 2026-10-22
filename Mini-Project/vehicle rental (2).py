"""
Vehicle Rental Management System
--------------------------------
Mini Project #21
Concepts : OOP, Inheritance, Database (SQLite), GUI (Tkinter)

Features : Add vehicles, rent a vehicle, return a vehicle (bill is
           calculated automatically), view fleet and rental history.
"""

import sqlite3
from datetime import date, datetime

DB_FILE = "vehicle_rental.db"


# ---------------------------------------------------------------
# 1. OOP + INHERITANCE
#    Vehicle is the parent class. Car, Bike and Truck inherit from
#    it and change how the rent is calculated (polymorphism).
# ---------------------------------------------------------------
class Vehicle:
    TYPE = "Vehicle"
    EXTRA_CHARGE = 0  # fixed extra charge added to every rental

    def __init__(self, reg_no, brand, rate_per_day, available=True, vehicle_id=None):
        self.vehicle_id = vehicle_id
        self.reg_no = reg_no
        self.brand = brand
        self.rate_per_day = rate_per_day
        self.available = available

    def calculate_rent(self, days):
        """Base rule: days x daily rate (+ any extra charge)."""
        return days * self.rate_per_day + self.EXTRA_CHARGE

    def __str__(self):
        return f"{self.TYPE}: {self.brand} ({self.reg_no})"


class Car(Vehicle):
    TYPE = "Car"
    EXTRA_CHARGE = 100  # cleaning / insurance fee


class Bike(Vehicle):
    TYPE = "Bike"

    def calculate_rent(self, days):
        rent = super().calculate_rent(days)
        return rent * 0.9 if days >= 7 else rent  # 10% weekly discount


class Truck(Vehicle):
    TYPE = "Truck"
    EXTRA_CHARGE = 500  # loading / permit fee


VEHICLE_CLASSES = {"Car": Car, "Bike": Bike, "Truck": Truck}


# ---------------------------------------------------------------
# 2. DATABASE LAYER (SQLite)
# ---------------------------------------------------------------
class Database:
    def __init__(self, filename=DB_FILE):
        self.conn = sqlite3.connect(filename)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS vehicles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vtype TEXT NOT NULL,
                reg_no TEXT UNIQUE NOT NULL,
                brand TEXT NOT NULL,
                rate_per_day REAL NOT NULL,
                available INTEGER NOT NULL DEFAULT 1)""")
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS rentals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vehicle_id INTEGER NOT NULL,
                customer TEXT NOT NULL,
                phone TEXT NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT,
                total REAL,
                FOREIGN KEY (vehicle_id) REFERENCES vehicles(id))""")
        self.conn.commit()

    def close(self):
        self.conn.close()


# ---------------------------------------------------------------
# 3. BUSINESS LOGIC
# ---------------------------------------------------------------
class RentalError(Exception):
    """Raised for any rule violation (bad input, vehicle unavailable...)."""


class RentalSystem:
    def __init__(self, db):
        self.db = db

    @staticmethod
    def _to_vehicle(row):
        cls = VEHICLE_CLASSES[row["vtype"]]
        return cls(row["reg_no"], row["brand"], row["rate_per_day"],
                   bool(row["available"]), row["id"])

    def add_vehicle(self, vtype, reg_no, brand, rate):
        reg_no, brand = reg_no.strip().upper(), brand.strip()
        if vtype not in VEHICLE_CLASSES:
            raise RentalError("Choose a valid vehicle type.")
        if not reg_no or not brand:
            raise RentalError("Registration number and brand are required.")
        try:
            rate = float(rate)
            if rate <= 0:
                raise ValueError
        except ValueError:
            raise RentalError("Rate must be a positive number.")
        try:
            self.db.conn.execute(
                "INSERT INTO vehicles (vtype, reg_no, brand, rate_per_day) "
                "VALUES (?,?,?,?)", (vtype, reg_no, brand, rate))
            self.db.conn.commit()
        except sqlite3.IntegrityError:
            raise RentalError(f"Vehicle {reg_no} already exists.")

    def get_vehicles(self, only_available=False):
        sql = "SELECT * FROM vehicles"
        if only_available:
            sql += " WHERE available = 1"
        rows = self.db.conn.execute(sql + " ORDER BY id").fetchall()
        return [(r["vtype"], self._to_vehicle(r)) for r in rows]

    def get_vehicle(self, vehicle_id):
        row = self.db.conn.execute(
            "SELECT * FROM vehicles WHERE id=?", (vehicle_id,)).fetchone()
        return self._to_vehicle(row) if row else None

    def rent_vehicle(self, vehicle_id, customer, phone, start=None):
        customer, phone = customer.strip(), phone.strip()
        if not customer:
            raise RentalError("Customer name is required.")
        if not (phone.isdigit() and len(phone) == 10):
            raise RentalError("Phone must be exactly 10 digits.")
        vehicle = self.get_vehicle(vehicle_id)
        if vehicle is None:
            raise RentalError("Vehicle not found.")
        if not vehicle.available:
            raise RentalError("This vehicle is already rented out.")
        start = start or date.today().isoformat()
        self.db.conn.execute(
            "INSERT INTO rentals (vehicle_id, customer, phone, start_date) "
            "VALUES (?,?,?,?)", (vehicle_id, customer, phone, start))
        self.db.conn.execute(
            "UPDATE vehicles SET available=0 WHERE id=?", (vehicle_id,))
        self.db.conn.commit()

    def return_vehicle(self, vehicle_id, end=None):
        """Close the open rental, calculate the bill and return it."""
        rental = self.db.conn.execute(
            "SELECT * FROM rentals WHERE vehicle_id=? AND end_date IS NULL",
            (vehicle_id,)).fetchone()
        if rental is None:
            raise RentalError("This vehicle is not currently rented.")
        end = end or date.today().isoformat()
        d1 = datetime.strptime(rental["start_date"], "%Y-%m-%d").date()
        d2 = datetime.strptime(end, "%Y-%m-%d").date()
        days = max((d2 - d1).days, 1)  # minimum charge: 1 day
        vehicle = self.get_vehicle(vehicle_id)
        total = vehicle.calculate_rent(days)  # polymorphism in action
        self.db.conn.execute(
            "UPDATE rentals SET end_date=?, total=? WHERE id=?",
            (end, total, rental["id"]))
        self.db.conn.execute(
            "UPDATE vehicles SET available=1 WHERE id=?", (vehicle_id,))
        self.db.conn.commit()
        return days, total

    def get_history(self):
        return self.db.conn.execute("""
            SELECT r.id, v.vtype, v.brand, v.reg_no, r.customer, r.phone,
                   r.start_date, r.end_date, r.total
            FROM rentals r JOIN vehicles v ON v.id = r.vehicle_id
            ORDER BY r.id DESC""").fetchall()


# ---------------------------------------------------------------
# 4. GUI (Tkinter)
# ---------------------------------------------------------------
def run_gui():
    import tkinter as tk
    from tkinter import ttk, messagebox

    class App:
        def __init__(self, root, system):
            self.root, self.system = root, system
            root.title("Vehicle Rental Management System")
            root.geometry("900x560")

            tk.Label(root, text="Vehicle Rental Management System",
                     font=("Arial", 18, "bold"), fg="#1b4f72").pack(pady=8)

            tabs = ttk.Notebook(root)
            tabs.pack(fill="both", expand=True, padx=10, pady=5)
            self.fleet_tab = ttk.Frame(tabs)
            self.rent_tab = ttk.Frame(tabs)
            self.hist_tab = ttk.Frame(tabs)
            tabs.add(self.fleet_tab, text="  Fleet  ")
            tabs.add(self.rent_tab, text="  Rent / Return  ")
            tabs.add(self.hist_tab, text="  History  ")
            tabs.bind("<<NotebookTabChanged>>", lambda e: self.refresh_all())

            self.build_fleet_tab()
            self.build_rent_tab()
            self.build_history_tab()
            self.refresh_all()

        # ---------- Fleet tab ----------
        def build_fleet_tab(self):
            f = tk.LabelFrame(self.fleet_tab, text="Add a vehicle", padx=8, pady=8)
            f.pack(fill="x", padx=10, pady=10)
            self.v_type = ttk.Combobox(f, values=list(VEHICLE_CLASSES),
                                       state="readonly", width=8)
            self.v_type.current(0)
            self.v_reg, self.v_brand, self.v_rate = (
                tk.Entry(f, width=14), tk.Entry(f, width=16), tk.Entry(f, width=8))
            for col, (label, w) in enumerate([("Type", self.v_type),
                                              ("Reg No", self.v_reg),
                                              ("Brand", self.v_brand),
                                              ("Rate/day", self.v_rate)]):
                tk.Label(f, text=label).grid(row=0, column=col * 2, padx=3)
                w.grid(row=0, column=col * 2 + 1, padx=3)
            tk.Button(f, text="Add", bg="#27ae60", fg="white",
                      command=self.on_add_vehicle).grid(row=0, column=8, padx=8)

            cols = ("ID", "Type", "Reg No", "Brand", "Rate/day", "Status")
            self.fleet_tree = self.make_tree(self.fleet_tab, cols, (40, 80, 120, 150, 90, 100))

        def on_add_vehicle(self):
            try:
                self.system.add_vehicle(self.v_type.get(), self.v_reg.get(),
                                        self.v_brand.get(), self.v_rate.get())
            except RentalError as e:
                return messagebox.showerror("Error", str(e))
            for w in (self.v_reg, self.v_brand, self.v_rate):
                w.delete(0, tk.END)
            self.refresh_all()

        # ---------- Rent / Return tab ----------
        def build_rent_tab(self):
            left = tk.LabelFrame(self.rent_tab, text="Rent a vehicle", padx=10, pady=10)
            left.pack(side="left", fill="both", expand=True, padx=10, pady=10)
            tk.Label(left, text="Vehicle").grid(row=0, column=0, sticky="w")
            self.rent_combo = ttk.Combobox(left, state="readonly", width=26)
            self.rent_combo.grid(row=0, column=1, pady=5)
            tk.Label(left, text="Customer name").grid(row=1, column=0, sticky="w")
            self.cust_name = tk.Entry(left, width=29)
            self.cust_name.grid(row=1, column=1, pady=5)
            tk.Label(left, text="Phone (10 digits)").grid(row=2, column=0, sticky="w")
            self.cust_phone = tk.Entry(left, width=29)
            self.cust_phone.grid(row=2, column=1, pady=5)
            tk.Button(left, text="Rent Now", bg="#2980b9", fg="white", width=14,
                      command=self.on_rent).grid(row=3, column=1, pady=10, sticky="e")

            right = tk.LabelFrame(self.rent_tab, text="Return a vehicle", padx=10, pady=10)
            right.pack(side="left", fill="both", expand=True, padx=10, pady=10)
            tk.Label(right, text="Vehicle").grid(row=0, column=0, sticky="w")
            self.return_combo = ttk.Combobox(right, state="readonly", width=26)
            self.return_combo.grid(row=0, column=1, pady=5)
            tk.Button(right, text="Return & Bill", bg="#e67e22", fg="white", width=14,
                      command=self.on_return).grid(row=1, column=1, pady=10, sticky="e")

        def on_rent(self):
            idx = self.rent_combo.current()
            if idx < 0:
                return messagebox.showwarning("Select", "Choose a vehicle first.")
            try:
                self.system.rent_vehicle(self.rent_ids[idx], self.cust_name.get(),
                                         self.cust_phone.get())
            except RentalError as e:
                return messagebox.showerror("Error", str(e))
            messagebox.showinfo("Done", "Vehicle rented successfully.")
            self.cust_name.delete(0, tk.END)
            self.cust_phone.delete(0, tk.END)
            self.refresh_all()

        def on_return(self):
            idx = self.return_combo.current()
            if idx < 0:
                return messagebox.showwarning("Select", "Choose a vehicle first.")
            try:
                days, total = self.system.return_vehicle(self.return_ids[idx])
            except RentalError as e:
                return messagebox.showerror("Error", str(e))
            messagebox.showinfo("Bill", f"Days rented: {days}\nTotal rent: Rs. {total:.2f}")
            self.refresh_all()

        # ---------- History tab ----------
        def build_history_tab(self):
            cols = ("#", "Type", "Brand", "Reg No", "Customer", "Phone",
                    "Start", "End", "Total")
            self.hist_tree = self.make_tree(self.hist_tab, cols,
                                            (35, 60, 100, 100, 110, 100, 90, 90, 80))

        # ---------- helpers ----------
        @staticmethod
        def make_tree(parent, cols, widths):
            tree = ttk.Treeview(parent, columns=cols, show="headings", height=14)
            for c, w in zip(cols, widths):
                tree.heading(c, text=c)
                tree.column(c, width=w, anchor="center")
            tree.pack(fill="both", expand=True, padx=10, pady=10)
            return tree

        def refresh_all(self):
            for t in (self.fleet_tree, self.hist_tree):
                t.delete(*t.get_children())
            fleet = self.system.get_vehicles()
            for vtype, v in fleet:
                status = "Available" if v.available else "Rented"
                self.fleet_tree.insert("", tk.END, values=(
                    v.vehicle_id, vtype, v.reg_no, v.brand, f"{v.rate_per_day:.0f}", status))
            for r in self.system.get_history():
                self.hist_tree.insert("", tk.END, values=(
                    r["id"], r["vtype"], r["brand"], r["reg_no"], r["customer"],
                    r["phone"], r["start_date"], r["end_date"] or "-",
                    f"{r['total']:.2f}" if r["total"] is not None else "-"))
            avail = [v for _, v in fleet if v.available]
            rented = [v for _, v in fleet if not v.available]
            self.rent_ids = [v.vehicle_id for v in avail]
            self.return_ids = [v.vehicle_id for v in rented]
            self.rent_combo["values"] = [str(v) for v in avail]
            self.return_combo["values"] = [str(v) for v in rented]
            self.rent_combo.set("")
            self.return_combo.set("")

    root = tk.Tk()
    db = Database()
    App(root, RentalSystem(db))
    root.mainloop()
    db.close()


if __name__ == "__main__":
    run_gui()

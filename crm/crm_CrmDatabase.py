import sqlite3
from sqlite3 import Error
from datetime import datetime

class CrmDatabase:
    """Handles all SQLite database interactions for the CRM."""
    
    def __init__(self, db_file="park.db"):
        self.db_file = db_file
        self.conn = None
        self.cursor = None

    def connect(self):
        """Establish a connection to the SQLite database if not already set."""
        if self.conn is None or self.cursor is None:
            try:
                self.conn = sqlite3.connect(self.db_file)
                self.cursor = self.conn.cursor()
            except Error as e:
                raise Exception(f"Database connection failed: {e}")

    def close(self):
        """Close the database connection if it exists."""
        if self.cursor:
            self.cursor.close()
            self.cursor = None
        if self.conn:
            self.conn.close()
            self.conn = None

    def add_customer(self, first_name, last_name, email, phone, address):
        """Add a new customer to the database."""
        try:
            self.connect()
            self.cursor.execute("""
                INSERT INTO customers (first_name, last_name, email, phone, address)
                VALUES (?, ?, ?, ?, ?)
            """, (first_name, last_name, email, phone, address))
            self.conn.commit()
            return self.cursor.lastrowid
        except Error as e:
            raise Exception(f"Failed to add customer: {e}")
        # Do not close connection in tests to maintain state

    def get_customer(self, customer_id):
        """Retrieve a customer by ID."""
        try:
            self.connect()
            self.cursor.execute("SELECT * FROM customers WHERE customer_id = ?", (customer_id,))
            return self.cursor.fetchone()
        except Error as e:
            raise Exception(f"Failed to retrieve customer: {e}")
        # Do not close connection in tests

    def add_reservation(self, customer_id, site_id, check_in_date, check_out_date, status, total_amount):
        """Add a new reservation to the database."""
        try:
            self.connect()
            self.cursor.execute("""
                INSERT INTO reservations (customer_id, site_id, check_in_date, check_out_date, status, total_amount)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (customer_id, site_id, check_in_date, check_out_date, status, total_amount))
            self.conn.commit()
            return self.cursor.lastrowid
        except Error as e:
            raise Exception(f"Failed to add reservation: {e}")
        # Do not close connection in tests

    def get_available_sites(self, check_in_date, check_out_date):
        """Retrieve available sites for a date range."""
        try:
            self.connect()
            self.cursor.execute("""
                SELECT site_id, site_number, site_type, daily_rate
                FROM rv_sites
                WHERE is_active = 1
                AND site_id NOT IN (
                    SELECT site_id
                    FROM reservations
                    WHERE status IN ('Confirmed', 'Checked-in')
                    AND check_in_date <= ? AND check_out_date >= ?
                )
            """, (check_out_date, check_in_date))
            return self.cursor.fetchall()
        except Error as e:
            raise Exception(f"Failed to retrieve available sites: {e}")
        # Do not close connection in tests

    def add_invoice(self, reservation_id, customer_id, issue_date, due_date, total_amount, status):
        """Add a new invoice to the database."""
        try:
            self.connect()
            self.cursor.execute("""
                INSERT INTO invoices (reservation_id, customer_id, issue_date, due_date, total_amount, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (reservation_id, customer_id, issue_date, due_date, total_amount, status))
            self.conn.commit()
            return self.cursor.lastrowid
        except Error as e:
            raise Exception(f"Failed to add invoice: {e}")
        # Do not close connection in tests

    def add_payment(self, invoice_id, customer_id, payment_date, amount, payment_method):
        """Add a new payment to the database."""
        try:
            self.connect()
            self.cursor.execute("""
                INSERT INTO payments (invoice_id, customer_id, payment_date, amount, payment_method)
                VALUES (?, ?, ?, ?, ?)
            """, (invoice_id, customer_id, payment_date, amount, payment_method))
            self.conn.commit()
            return self.cursor.lastrowid
        except Error as e:
            raise Exception(f"Failed to add payment: {e}")
        # Do not close connection in tests
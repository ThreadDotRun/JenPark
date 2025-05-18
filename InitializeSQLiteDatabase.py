import sqlite3
from sqlite3 import Error

class InitializeSQLiteDatabase:
    def __init__(self, db_file="park.db"):
        """Initialize the database connection."""
        self.db_file = db_file
        self.conn = None
        self.cursor = None

    def connect(self):
        """Create a database connection to the SQLite database."""
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.cursor = self.conn.cursor()
            print(f"Connected to SQLite database: {self.db_file}")
        except Error as e:
            print(f"Error connecting to database: {e}")
            raise

    def create_tables(self):
        """Create the necessary tables if they do not exist."""
        try:
            # Table for customers
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS customers (
                    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email TEXT UNIQUE,
                    phone TEXT,
                    address TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Table for RV sites
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS rv_sites (
                    site_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    site_number TEXT NOT NULL UNIQUE,
                    site_type TEXT NOT NULL,
                    daily_rate REAL NOT NULL,
                    is_active INTEGER NOT NULL DEFAULT 1,
                    description TEXT
                )
            """)

            # Table for reservations
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS reservations (
                    reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id INTEGER NOT NULL,
                    site_id INTEGER NOT NULL,
                    check_in_date DATE NOT NULL,
                    check_out_date DATE NOT NULL,
                    status TEXT NOT NULL,
                    total_amount REAL NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
                    FOREIGN KEY (site_id) REFERENCES rv_sites(site_id),
                    CHECK (check_out_date > check_in_date)
                )
            """)

            # Table for invoices
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS invoices (
                    invoice_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    reservation_id INTEGER NOT NULL,
                    customer_id INTEGER NOT NULL,
                    issue_date DATE NOT NULL,
                    due_date DATE NOT NULL,
                    total_amount REAL NOT NULL,
                    status TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (reservation_id) REFERENCES reservations(reservation_id),
                    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
                )
            """)

            # Table for payments
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS payments (
                    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    invoice_id INTEGER NOT NULL,
                    customer_id INTEGER NOT NULL,
                    payment_date DATE NOT NULL,
                    amount REAL NOT NULL,
                    payment_method TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (invoice_id) REFERENCES invoices(invoice_id),
                    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
                )
            """)

            self.conn.commit()
            print("Tables created successfully or already exist.")
        except Error as e:
            print(f"Error creating tables: {e}")
            raise

    def close(self):
        """Close the database connection."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("Database connection closed.")

    def initialize(self):
        """Connect to the database and create tables."""
        try:
            self.connect()
            self.create_tables()
        finally:
            self.close()

if __name__ == "__main__":
    # Example usage
    db_initializer = InitializeSQLiteDatabase()
    db_initializer.initialize()
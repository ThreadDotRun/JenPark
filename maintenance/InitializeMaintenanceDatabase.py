import sqlite3
from sqlite3 import Error

class InitializeMaintenanceDatabase:
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
        """Create the maintenance and facility management tables if they do not exist."""
        try:
            # Table for facilities
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS facilities (
                    facility_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    facility_name TEXT NOT NULL,
                    facility_type TEXT NOT NULL,
                    location TEXT,
                    is_active INTEGER NOT NULL DEFAULT 1,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Table for assets
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS assets (
                    asset_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    facility_id INTEGER NOT NULL,
                    asset_name TEXT NOT NULL,
                    asset_type TEXT NOT NULL,
                    serial_number TEXT,
                    purchase_date DATE,
                    is_active INTEGER NOT NULL DEFAULT 1,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (facility_id) REFERENCES facilities(facility_id)
                )
            """)

            # Table for maintenance requests
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS maintenance_requests (
                    request_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    facility_id INTEGER,
                    asset_id INTEGER,
                    customer_id INTEGER,
                    request_date DATE NOT NULL,
                    priority TEXT NOT NULL,
                    status TEXT NOT NULL,
                    description TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (facility_id) REFERENCES facilities(facility_id),
                    FOREIGN KEY (asset_id) REFERENCES assets(asset_id),
                    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
                    CHECK (facility_id IS NOT NULL OR asset_id IS NOT NULL)
                )
            """)

            # Table for maintenance schedules
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS maintenance_schedules (
                    schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    facility_id INTEGER,
                    asset_id INTEGER,
                    task_name TEXT NOT NULL,
                    frequency TEXT NOT NULL,
                    next_due_date DATE NOT NULL,
                    status TEXT NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (facility_id) REFERENCES facilities(facility_id),
                    FOREIGN KEY (asset_id) REFERENCES assets(asset_id),
                    CHECK (facility_id IS NOT NULL OR asset_id IS NOT NULL)
                )
            """)

            # Table for maintenance logs
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS maintenance_logs (
                    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    request_id INTEGER,
                    schedule_id INTEGER,
                    facility_id INTEGER,
                    asset_id INTEGER,
                    completion_date DATE NOT NULL,
                    performed_by TEXT NOT NULL,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (request_id) REFERENCES maintenance_requests(request_id),
                    FOREIGN KEY (schedule_id) REFERENCES maintenance_schedules(schedule_id),
                    FOREIGN KEY (facility_id) REFERENCES facilities(facility_id),
                    FOREIGN KEY (asset_id) REFERENCES assets(asset_id),
                    CHECK (facility_id IS NOT NULL OR asset_id IS NOT NULL)
                )
            """)

            self.conn.commit()
            print("Maintenance tables created successfully or already exist.")
        except Error as e:
            print(f"Error creating maintenance tables: {e}")
            raise

    def close(self):
        """Close the database connection."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("Database connection closed.")

    def initialize(self):
        """Connect to the database and create maintenance tables."""
        try:
            self.connect()
            self.create_tables()
        finally:
            self.close()

if __name__ == "__main__":
    # Example usage
    db_initializer = InitializeMaintenanceDatabase()
    db_initializer.initialize()
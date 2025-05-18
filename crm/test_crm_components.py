import unittest
import sqlite3
import os
from datetime import datetime, timedelta
from unittest.mock import patch
from crm_CrmDatabase import CrmDatabase
from crm_CrmService import CrmService
from crm_CrmValidator import CrmValidator
from crm_CrmErrorHandler import CrmErrorHandler

class TestCrmComponents(unittest.TestCase):
    def setUp(self):
        """Set up a file-based database and initialize schema before each test."""
        # Use a file-based database
        self.db_file = "test_park.db"
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        
        # Initialize CrmDatabase with the existing connection
        self.db = CrmDatabase(self.db_file)
        self.db.conn = self.conn
        self.db.cursor = self.cursor
        
        # Create tables (same schema as InitializeSQLiteDatabase.py)
        self.cursor.executescript("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT UNIQUE,
                phone TEXT,
                address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS rv_sites (
                site_id INTEGER PRIMARY KEY AUTOINCREMENT,
                site_number TEXT NOT NULL UNIQUE,
                site_type TEXT NOT NULL,
                daily_rate REAL NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 1,
                description TEXT
            );
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
            );
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
            );
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
            );
        """)
        
        # Insert sample RV sites
        self.cursor.executemany(
            "INSERT OR IGNORE INTO rv_sites (site_number, site_type, daily_rate, is_active) VALUES (?, ?, ?, ?)",
            [
                ("Site1", "Full Hookup", 50.0, 1),
                ("Site2", "Tent", 30.0, 1),
                ("Site3", "Pull-through", 60.0, 0)  # Inactive site
            ]
        )
        self.conn.commit()
        
        # Initialize CrmService with the same connection
        self.service = CrmService(self.db_file)
        self.service.db.conn = self.conn
        self.service.db.cursor = self.cursor
        
        self.validator = CrmValidator()
        self.error_handler = CrmErrorHandler()

    def tearDown(self):
        """Close database connection and remove the test database file."""
        if self.conn:
            self.conn.close()
        if os.path.exists(self.db_file):
            os.remove(self.db_file)

    # CrmDatabase Tests
    def test_add_customer_success(self):
        """Test adding a valid customer."""
        customer_id = self.db.add_customer("John", "Doe", "john.doe@example.com", "+12345678901", "123 Main St")
        self.cursor.execute("SELECT * FROM customers WHERE customer_id = ?", (customer_id,))
        customer = self.cursor.fetchone()
        self.assertEqual(customer[1], "John")
        self.assertEqual(customer[2], "Doe")
        self.assertEqual(customer[3], "john.doe@example.com")

    def test_add_customer_duplicate_email(self):
        """Test adding a customer with a duplicate email."""
        self.db.add_customer("John", "Doe", "john.doe@example.com", "+12345678901", "123 Main St")
        with self.assertRaises(Exception) as context:
            self.db.add_customer("Jane", "Doe", "john.doe@example.com", "+12345678902", "456 Main St")
        self.assertIn("UNIQUE constraint failed", str(context.exception))

    def test_get_customer_success(self):
        """Test retrieving a customer by ID."""
        customer_id = self.db.add_customer("John", "Doe", "john.doe@example.com", "+12345678901", "123 Main St")
        customer = self.db.get_customer(customer_id)
        self.assertEqual(customer[1], "John")
        self.assertEqual(customer[2], "Doe")

    def test_add_reservation_success(self):
        """Test adding a valid reservation."""
        customer_id = self.db.add_customer("John", "Doe", "john.doe@example.com", "+12345678901", "123 Main St")
        reservation_id = self.db.add_reservation(customer_id, 1, "2025-06-01", "2025-06-05", "Confirmed", 200.0)
        self.cursor.execute("SELECT * FROM reservations WHERE reservation_id = ?", (reservation_id,))
        reservation = self.cursor.fetchone()
        self.assertEqual(reservation[1], customer_id)
        self.assertEqual(reservation[2], 1)
        self.assertEqual(reservation[6], 200.0)

    def test_get_available_sites_success(self):
        """Test retrieving available sites."""
        customer_id = self.db.add_customer("John", "Doe", "john.doe@example.com", "+12345678901", "123 Main St")
        self.db.add_reservation(customer_id, 1, "2025-06-01", "2025-06-05", "Confirmed", 200.0)
        sites = self.db.get_available_sites("2025-06-01", "2025-06-05")
        self.assertEqual(len(sites), 1)  # Only Site2 should be available (Site3 is inactive)
        self.assertEqual(sites[0][1], "Site2")

    def test_add_invoice_success(self):
        """Test adding a valid invoice."""
        customer_id = self.db.add_customer("John", "Doe", "john.doe@example.com", "+12345678901", "123 Main St")
        reservation_id = self.db.add_reservation(customer_id, 1, "2025-06-01", "2025-06-05", "Confirmed", 200.0)
        invoice_id = self.db.add_invoice(reservation_id, customer_id, "2025-05-18", "2025-05-25", 200.0, "Pending")
        self.cursor.execute("SELECT reservation_id, total_amount, status FROM invoices WHERE invoice_id = ?", (invoice_id,))
        invoice = self.cursor.fetchone()
        self.assertEqual(invoice[0], reservation_id)
        self.assertEqual(invoice[1], 200.0)
        self.assertEqual(invoice[2], "Pending")

    def test_add_payment_success(self):
        """Test adding a valid payment."""
        customer_id = self.db.add_customer("John", "Doe", "john.doe@example.com", "+12345678901", "123 Main St")
        reservation_id = self.db.add_reservation(customer_id, 1, "2025-06-01", "2025-06-05", "Confirmed", 200.0)
        invoice_id = self.db.add_invoice(reservation_id, customer_id, "2025-05-18", "2025-05-25", 200.0, "Pending")
        payment_id = self.db.add_payment(invoice_id, customer_id, "2025-05-18", 200.0, "Credit Card")
        self.cursor.execute("SELECT * FROM payments WHERE payment_id = ?", (payment_id,))
        payment = self.cursor.fetchone()
        self.assertEqual(payment[1], invoice_id)
        self.assertEqual(payment[4], 200.0)

    # CrmService Tests
    def test_create_customer_success(self):
        """Test creating a customer via CrmService."""
        result = self.service.create_customer("John", "Doe", "john.doe@example.com", "+12345678901", "123 Main St")
        self.assertEqual(result["status"], "success")
        self.assertTrue(isinstance(result["customer_id"], int))

    def test_create_customer_invalid_email(self):
        """Test creating a customer with invalid email."""
        result = self.service.create_customer("John", "Doe", "invalid_email", "+12345678901", "123 Main St")
        self.assertEqual(result["status"], "error")
        self.assertIn("Invalid email format", result["message"])

    def test_create_reservation_success(self):
        """Test creating a reservation via CrmService."""
        customer_id = self.db.add_customer("John", "Doe", "john.doe@example.com", "+12345678901", "123 Main St")
        result = self.service.create_reservation(customer_id, 1, "2025-06-01", "2025-06-05")
        self.assertEqual(result["status"], "success")
        self.assertTrue(isinstance(result["reservation_id"], int))
        self.assertTrue(isinstance(result["invoice_id"], int))

    def test_create_reservation_past_date(self):
        """Test creating a reservation with a past date."""
        customer_id = self.db.add_customer("John", "Doe", "john.doe@example.com", "+12345678901", "123 Main St")
        result = self.service.create_reservation(customer_id, 1, "2025-05-01", "2025-05-05")
        self.assertEqual(result["status"], "error")
        self.assertIn("Check-in date cannot be in the past", result["message"])

    def test_record_payment_success(self):
        """Test recording a payment via CrmService."""
        customer_id = self.db.add_customer("John", "Doe", "john.doe@example.com", "+12345678901", "123 Main St")
        reservation_id = self.db.add_reservation(customer_id, 1, "2025-06-01", "2025-06-05", "Confirmed", 200.0)
        invoice_id = self.db.add_invoice(reservation_id, customer_id, "2025-05-18", "2025-05-25", 200.0, "Pending")
        result = self.service.record_payment(invoice_id, customer_id, 200.0, "Credit Card")
        self.assertEqual(result["status"], "success")
        self.assertTrue(isinstance(result["payment_id"], int))

    def test_get_available_sites_success(self):
        """Test retrieving available sites via CrmService."""
        customer_id = self.db.add_customer("John", "Doe", "john.doe@example.com", "+12345678901", "123 Main St")
        self.db.add_reservation(customer_id, 1, "2025-06-01", "2025-06-05", "Confirmed", 200.0)
        result = self.service.get_available_sites("2025-06-01", "2025-06-05")
        self.assertEqual(result["status"], "success")
        self.assertEqual(len(result["sites"]), 1)
        self.assertEqual(result["sites"][0][1], "Site2")

    # CrmValidator Tests
    def test_validate_customer_data_success(self):
        """Test validating valid customer data."""
        self.validator.validate_customer_data("John", "Doe", "john.doe@example.com", "+12345678901", "123 Main St")
        self.assertTrue(True)  # No exception means success

    def test_validate_customer_data_invalid_email(self):
        """Test validating customer data with invalid email."""
        with self.assertRaises(ValueError) as context:
            self.validator.validate_customer_data("John", "Doe", "invalid_email", "+12345678901", "123 Main St")
        self.assertEqual(str(context.exception), "Invalid email format")

    def test_validate_reservation_data_success(self):
        """Test validating valid reservation data."""
        self.validator.validate_reservation_data(1, 1, "2025-06-01", "2025-06-05")
        self.assertTrue(True)

    def test_validate_reservation_data_invalid_dates(self):
        """Test validating reservation data with invalid dates."""
        with self.assertRaises(ValueError) as context:
            self.validator.validate_reservation_data(1, 1, "2025-06-05", "2025-06-01")
        self.assertEqual(str(context.exception), "Check-out date must be after check-in date")

    def test_validate_payment_data_success(self):
        """Test validating valid payment data."""
        self.validator.validate_payment_data(1, 1, 100.0, "Credit Card")
        self.assertTrue(True)

    def test_validate_payment_data_invalid_method(self):
        """Test validating payment data with invalid payment method."""
        with self.assertRaises(ValueError) as context:
            self.validator.validate_payment_data(1, 1, 100.0, "Invalid")
        self.assertEqual(str(context.exception), "Invalid payment method")

    # CrmErrorHandler Tests
    def test_handle_error(self):
        """Test error handling and logging."""
        exception = ValueError("Test error")
        result = self.error_handler.handle_error(exception, "Test context")
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["message"], "Test context: Test error")

    # Mocking Database Failure
    @patch('sqlite3.connect')
    def test_database_connection_failure(self, mock_connect):
        """Test handling database connection failure."""
        mock_connect.side_effect = sqlite3.Error("Connection failed")
        service = CrmService("test_park.db")
        result = service.create_customer("John", "Doe", "john.doe@example.com", "+12345678901", "123 Main St")
        self.assertEqual(result["status"], "error")
        self.assertIn("Database connection failed", result["message"])

if __name__ == '__main__':
    unittest.main()
from datetime import datetime
import re

class CrmValidator:
    """Validates input data for CRM operations."""
    
    def validate_customer_data(self, first_name, last_name, email, phone, address):
        """Validate customer data."""
        if not first_name or not isinstance(first_name, str) or len(first_name.strip()) == 0:
            raise ValueError("First name is required and must be a non-empty string")
        if not last_name or not isinstance(last_name, str) or len(last_name.strip()) == 0:
            raise ValueError("Last name is required and must be a non-empty string")
        if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")
        if phone and not re.match(r"^\+?\d{10,15}$", phone):
            raise ValueError("Invalid phone number format")

    def validate_reservation_data(self, customer_id, site_id, check_in_date, check_out_date):
        """Validate reservation data."""
        if not isinstance(customer_id, int) or customer_id <= 0:
            raise ValueError("Invalid customer ID")
        if not isinstance(site_id, int) or site_id <= 0:
            raise ValueError("Invalid site ID")
        self.validate_date_range(check_in_date, check_out_date)

    def validate_payment_data(self, invoice_id, customer_id, amount, payment_method):
        """Validate payment data."""
        if not isinstance(invoice_id, int) or invoice_id <= 0:
            raise ValueError("Invalid invoice ID")
        if not isinstance(customer_id, int) or customer_id <= 0:
            raise ValueError("Invalid customer ID")
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Amount must be a positive number")
        if payment_method not in ["Cash", "Credit Card", "Check"]:
            raise ValueError("Invalid payment method")

    def validate_date_range(self, check_in_date, check_out_date):
        """Validate date range for reservations."""
        try:
            check_in = datetime.strptime(check_in_date, "%Y-%m-%d")
            check_out = datetime.strptime(check_out_date, "%Y-%m-%d")
            if check_in >= check_out:
                raise ValueError("Check-out date must be after check-in date")
            if check_in < datetime.now().replace(hour=0, minute=0, second=0, microsecond=0):
                raise ValueError("Check-in date cannot be in the past")
        except ValueError as e:
            if "strptime" in str(e):
                raise ValueError("Dates must be in YYYY-MM-DD format")
            raise
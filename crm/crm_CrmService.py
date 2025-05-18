from datetime import datetime, timedelta
from crm_CrmDatabase import CrmDatabase
from crm_CrmValidator import CrmValidator
from crm_CrmErrorHandler import CrmErrorHandler

class CrmService:
    """Handles business logic for CRM operations."""
    
    def __init__(self, db_file="park.db"):
        self.db = CrmDatabase(db_file)
        self.validator = CrmValidator()
        self.error_handler = CrmErrorHandler()

    def create_customer(self, first_name, last_name, email, phone, address):
        """Create a new customer after validation."""
        try:
            self.validator.validate_customer_data(first_name, last_name, email, phone, address)
            customer_id = self.db.add_customer(first_name, last_name, email, phone, address)
            return {"status": "success", "customer_id": customer_id}
        except Exception as e:
            return self.error_handler.handle_error(e, "Failed to create customer")

    def create_reservation(self, customer_id, site_id, check_in_date, check_out_date):
        """Create a reservation with calculated cost."""
        try:
            self.validator.validate_reservation_data(customer_id, site_id, check_in_date, check_out_date)
            check_in = datetime.strptime(check_in_date, "%Y-%m-%d")
            check_out = datetime.strptime(check_out_date, "%Y-%m-%d")
            days = (check_out - check_in).days
            
            # Get site details to calculate cost
            self.db.connect()
            self.db.cursor.execute("SELECT daily_rate FROM rv_sites WHERE site_id = ?", (site_id,))
            daily_rate = self.db.cursor.fetchone()[0]
            self.db.close()
            
            total_amount = daily_rate * days
            reservation_id = self.db.add_reservation(customer_id, site_id, check_in_date, check_out_date, "Confirmed", total_amount)
            
            # Create invoice
            issue_date = datetime.now().strftime("%Y-%m-%d")
            due_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
            invoice_id = self.db.add_invoice(reservation_id, customer_id, issue_date, due_date, total_amount, "Pending")
            
            return {"status": "success", "reservation_id": reservation_id, "invoice_id": invoice_id}
        except Exception as e:
            return self.error_handler.handle_error(e, "Failed to create reservation")

    def record_payment(self, invoice_id, customer_id, amount, payment_method):
        """Record a payment for an invoice."""
        try:
            self.validator.validate_payment_data(invoice_id, customer_id, amount, payment_method)
            payment_date = datetime.now().strftime("%Y-%m-%d")
            payment_id = self.db.add_payment(invoice_id, customer_id, payment_date, amount, payment_method)
            
            # Update invoice status
            self.db.connect()
            self.db.cursor.execute("UPDATE invoices SET status = 'Paid' WHERE invoice_id = ?", (invoice_id,))
            self.db.conn.commit()
            self.db.close()
            
            return {"status": "success", "payment_id": payment_id}
        except Exception as e:
            return self.error_handler.handle_error(e, "Failed to record payment")

    def get_available_sites(self, check_in_date, check_out_date):
        """Get available sites for a date range."""
        try:
            self.validator.validate_date_range(check_in_date, check_out_date)
            sites = self.db.get_available_sites(check_in_date, check_out_date)
            return {"status": "success", "sites": sites}
        except Exception as e:
            return self.error_handler.handle_error(e, "Failed to retrieve available sites")
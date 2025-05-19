# RV Park CRM/Maintenance System

## Overview
The RV Park CRM/Maintenance System is a Python-based framework designed to manage operations for an RV park, including customer management, site reservations, invoicing, payment tracking, and maintenance/facility management. The system uses SQLite for data storage and is organized into core database initialization components and modular packages (`crm/` and `maintenance/`). Comprehensive unit tests ensure reliability and correctness of the system.

### Project Structure
```
|-- InitializeSQLiteDatabase.py
|-- Maintenance Database Schema.txt
|-- README.md
|-- crm/
    |-- __init__.py
    |-- crm_CrmDatabase.py
    |-- crm_CrmErrorHandler.py
    |-- crm_CrmService.py
    |-- crm_CrmValidator.py
    |-- test_crm_components.py
|-- maintenance/
    |-- __init__.py
    |-- InitializeMaintenanceDatabase.py
|-- requirements.txt
```

- **InitializeSQLiteDatabase.py**: Initializes the SQLite database (`park.db`) with tables for CRM operations.
- **Maintenance Database Schema.txt**: Contains the raw SQL schema for maintenance and facility management tables.
- **crm/**: Contains the CRM module with components for database interactions, business logic, input validation, error handling, and unit tests.
- **maintenance/**: Contains the Maintenance and Facility Management module for initializing maintenance-related tables.
- **README.md**: This documentation file.

## Features
- **Database Management**: Creates and manages tables for customers, RV sites, reservations, invoices, payments, facilities, assets, maintenance requests, schedules, and logs with foreign key constraints for data integrity.
- **Customer Management**: Add and retrieve customer information with validation for names, email, and phone numbers.
- **Reservation System**: Create reservations, calculate costs based on site daily rates, and check site availability for date ranges.
- **Invoicing and Payments**: Generate invoices for reservations and record payments, updating invoice status automatically.
- **Maintenance and Facility Management**: Initialize tables to manage park facilities, assets, maintenance requests, schedules, and logs.
- **Input Validation**: Ensures data integrity with checks for email formats, phone numbers, date ranges, and payment methods.
- **Error Handling**: Centralized error logging to `crm_errors.log` with standardized error responses.
- **Unit Testing**: Comprehensive tests covering all CRM components, using a file-based test database (`test_park.db`).

## Requirements
- Python 3.6 or higher
- SQLite3 (included with Python standard library)
- pathspec==0.12.1

## Setup Instructions
1. **Clone or Download the Repository**:
   - Ensure all files are in the project directory with the structure shown above.
2. **Activate Virtual Environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Initialize the Database**:
   - Run the CRM database initialization script to create `park.db` with CRM tables:
     ```bash
     python InitializeSQLiteDatabase.py
     ```
   - Run the maintenance database initialization script to add maintenance tables to `park.db`:
     ```bash
     python maintenance/InitializeMaintenanceDatabase.py
     ```
   - These scripts create the database and tables in the project root directory.
5. **Verify Permissions**:
   - Ensure write permissions in the project directory for creating `park.db`, `test_park.db` (for tests), and `crm_errors.log` (for error logging).

## Components

### InitializeSQLiteDatabase
- **File**: `InitializeSQLiteDatabase.py`
- **Purpose**: Sets up the SQLite database (`park.db`) with tables for `customers`, `rv_sites`, `reservations`, `invoices`, and `payments`.
- **Features**:
  - Uses `CREATE TABLE IF NOT EXISTS` for idempotent table creation.
  - Defines foreign keys and constraints (e.g., `CHECK (check_out_date > check_in_date)`).
  - Includes error handling for connection and table creation.
  - Automatically closes connections to prevent resource leaks.
- **Usage**:
  ```python
  from InitializeSQLiteDatabase import InitializeSQLiteDatabase
  db_initializer = InitializeSQLiteDatabase()
  db_initializer.initialize()
  ```
- **Output**: Creates `park.db` and prints status messages (e.g., "Tables created successfully").

### InitializeMaintenanceDatabase
- **File**: `maintenance/InitializeMaintenanceDatabase.py`
- **Purpose**: Extends `park.db` with tables for `facilities`, `assets`, `maintenance_requests`, `maintenance_schedules`, and `maintenance_logs`.
- **Features**:
  - Uses `CREATE TABLE IF NOT EXISTS` for idempotent table creation.
  - Defines foreign keys to `facilities`, `assets`, and `customers` tables, with `CHECK` constraints (e.g., ensuring at least one of `facility_id` or `asset_id` is provided).
  - Includes error handling for connection and table creation.
  - Automatically closes connections to prevent resource leaks.
- **Usage**:
  ```python
  from maintenance.InitializeMaintenanceDatabase import InitializeMaintenanceDatabase
  db_initializer = InitializeMaintenanceDatabase()
  db_initializer.initialize()
  ```
- **Output**: Adds maintenance tables to `park.db` and prints status messages (e.g., "Maintenance tables created successfully").

### CRM Module
The `crm/` directory contains the core CRM functionality, organized as a Python package.

#### CrmDatabase
- **File**: `crm/crm_CrmDatabase.py`
- **Purpose**: Handles all SQLite database interactions for CRM operations.
- **Features**:
  - Methods to add customers, reservations, invoices, and payments.
  - Queries available RV sites for a given date range, excluding booked or inactive sites.
  - Reuses connections in tests to maintain state.
  - Robust error handling with descriptive exceptions.
- **Key Methods**:
  - `add_customer(first_name, last_name, email, phone, address)`
  - `add_reservation(customer_id, site_id, check_in_date, check_out_date, status, total_amount)`
  - `get_available_sites(check_in_date, check_out_date)`
  - `add_invoice(reservation_id, customer_id, issue_date, due_date, total_amount, status)`
  - `add_payment(invoice_id, customer_id, payment_date, amount, payment_method)`

#### CrmService
- **File**: `crm/crm_CrmService.py`
- **Purpose**: Implements business logic for CRM operations.
- **Features**:
  - Creates customers with validation and database insertion.
  - Manages reservations, calculating costs based on site daily rates and creating associated invoices.
  - Records payments and updates invoice status to "Paid".
  - Retrieves available sites with validation for date ranges.
  - Integrates with `CrmValidator` and `CrmErrorHandler` for robust operation.
- **Key Methods**:
  - `create_customer(first_name, last_name, email, phone, address)`
  - `create_reservation(customer_id, site_id, check_in_date, check_out_date)`
  - `record_payment(invoice_id, customer_id, amount, payment_method)`
  - `get_available_sites(check_in_date, check_out_date)`

#### CrmValidator
- **File**: `crm/crm_CrmValidator.py`
- **Purpose**: Validates input data to ensure data integrity.
- **Features**:
  - Validates customer data (names, email, phone).
  - Checks reservation data (customer ID, site ID, date ranges).
  - Verifies payment data (invoice ID, customer ID, amount, payment method).
  - Ensures dates are in `YYYY-MM-DD` format and check-in dates are not in the past.
- **Key Methods**:
  - `validate_customer_data(first_name, last_name, email, phone, address)`
  - `validate_reservation_data(customer_id, site_id, check_in_date, check_out_date)`
  - `validate_payment_data(invoice_id, customer_id, amount, payment_method)`
  - `validate_date_range(check_in_date, check_out_date)`

#### CrmErrorHandler
- **File**: `crm/crm_CrmErrorHandler.py`
- **Purpose**: Centralizes error handling and logging for CRM operations.
- **Features**:
  - Logs errors to `crm_errors.log` with timestamps and context.
  - Returns standardized error responses with status and message.
- **Key Method**:
  - `handle_error(exception, context)`

#### Unit Tests
- **File**: `crm/test_crm_components.py`
- **Purpose**: Tests all CRM components to ensure correctness.
- **Features**:
  - 20 unit tests covering `CrmDatabase`, `CrmService`, `CrmValidator`, and `CrmErrorHandler`.
  - Uses a file-based test database (`test_park.db`), created and deleted for each test run.
  - Tests database operations (e.g., adding customers, reservations), service logic (e.g., cost calculation), validation rules, and error handling.
  - Includes mock tests for database connection failures.
- **Recent Changes**:
  - Switched from in-memory to file-based database (`test_park.db`) for more reliable testing.
  - Fixed column indexing in `test_add_invoice_success` to correctly verify invoice data.
  - Resolved connection issues by reusing a single connection in tests.
  - Corrected import errors and schema initialization.

## Running Tests
The unit tests verify the functionality of all CRM components using a file-based SQLite database (`test_park.db`), which is created and deleted for each test run to ensure a clean state.

1. **Navigate to the `crm/` Directory**:
   ```bash
   cd crm
   ```
2. **Run the Tests**:
   ```bash
   python test_crm_components.py
   ```
3. **Alternative Commands**:
   - From the project root:
     ```bash
     python ./crm/test_crm_components.py
     ```
   - As a module:
     ```bash
     python -m crm.test_crm_components
     ```
4. **Expected Output**:
   ```
   ....................
   ----------------------------------------------------------------------
   Ran 20 tests in 23.791s

   OK
   ```
5. **Notes**:
   - Ensure write permissions in `crm/` for creating `test_park.db` and `crm_errors.log`.
   - Run tests in a virtual environment for consistency.
   - Use verbose mode to see individual test results:
     ```bash
     python test_crm_components.py -v
     ```

## Usage Example
```python
from InitializeSQLiteDatabase import InitializeSQLiteDatabase
from maintenance.InitializeMaintenanceDatabase import InitializeMaintenanceDatabase
from crm.crm_CrmService import CrmService

# Initialize the CRM database
db_initializer = InitializeSQLiteDatabase()
db_initializer.initialize()

# Initialize the maintenance database
maintenance_initializer = InitializeMaintenanceDatabase()
maintenance_initializer.initialize()

# Use the CRM service
crm = CrmService()
result = crm.create_customer("John", "Doe", "john.doe@example.com", "+12345678901", "123 Main St")
print(result)  # {'status': 'success', 'customer_id': 1}

result = crm.create_reservation(1, 1, "2025-06-01", "2025-06-05")
print(result)  # {'status': 'success', 'reservation_id': 1, 'invoice_id': 1}
```

## Database Tables Initialization Raw SQL
### RV Park CRM/ERP Database Schema
This section describes the current database schema for the RV Park CRM/ERP system, implemented in the SQLite database `park.db`. The schema consists of ten tables across two modules: CRM (`customers`, `rv_sites`, `reservations`, `invoices`, `payments`) and Maintenance (`facilities`, `assets`, `maintenance_requests`, `maintenance_schedules`, `maintenance_logs`). Each table is detailed below, including column names, data types, constraints, and relationships.

#### Table: customers
Stores information about customers of the RV park.

| Column Name   | Data Type | Constraints                                      | Description                              |
|---------------|-----------|--------------------------------------------------|------------------------------------------|
| customer_id   | INTEGER   | PRIMARY KEY AUTOINCREMENT                        | Unique identifier for the customer       |
| first_name    | TEXT      | NOT NULL                                         | Customer's first name                   |
| last_name     | TEXT      | NOT NULL                                         | Customer's last name                    |
| email         | TEXT      | UNIQUE                                           | Customer's email address (optional)      |
| phone         | TEXT      |                                                  | Customer's phone number (optional)       |
| address       | TEXT      |                                                  | Customer's address (optional)            |
| created_at    | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP                        | Timestamp of record creation             |

**Relationships**:
- Referenced by `reservations.customer_id`, `invoices.customer_id`, `payments.customer_id`, and `maintenance_requests.customer_id` (foreign keys).

#### Table: rv_sites
Stores information about RV sites available at the park.

| Column Name   | Data Type | Constraints                                      | Description                              |
|---------------|-----------|--------------------------------------------------|------------------------------------------|
| site_id       | INTEGER   | PRIMARY KEY AUTOINCREMENT                        | Unique identifier for the RV site        |
| site_number   | TEXT      | NOT NULL UNIQUE                                  | Unique site number (e.g., "Site1")       |
| site_type     | TEXT      | NOT NULL                                         | Type of site (e.g., "Full Hookup")       |
| daily_rate    | REAL      | NOT NULL                                         | Daily rental rate for the site           |
| is_active     | INTEGER   | NOT NULL DEFAULT 1                               | Site availability (1 = active, 0 = inactive) |
| description   | TEXT      |                                                  | Optional description of the site         |

**Relationships**:
- Referenced by `reservations.site_id` (foreign key).

#### Table: reservations
Stores reservation details for RV sites.

| Column Name     | Data Type | Constraints                                      | Description                              |
|-----------------|-----------|--------------------------------------------------|------------------------------------------|
| reservation_id  | INTEGER   | PRIMARY KEY AUTOINCREMENT                        | Unique identifier for the reservation    |
| customer_id     | INTEGER   | NOT NULL FOREIGN KEY REFERENCES customers(customer_id) | ID of the customer making the reservation |
| site_id         | INTEGER   | NOT NULL FOREIGN KEY REFERENCES rv_sites(site_id) | ID of the reserved RV site              |
| check_in_date   | DATE      | NOT NULL                                         | Date of check-in                        |
| check_out_date  | DATE      | NOT NULL                                         | Date of check-out                       |
| status          | TEXT      | NOT NULL                                         | Reservation status (e.g., "Confirmed")   |
| total_amount    | REAL      | NOT NULL                                         | Total cost of the reservation            |
| created_at      | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP                        | Timestamp of record creation             |

**Constraints**:
- `CHECK (check_out_date > check_in_date)`: Ensures check-out date is after check-in date.

**Relationships**:
- References `customers.customer_id` and `rv_sites.site_id` (foreign keys).
- Referenced by `invoices.reservation_id` (foreign key).

#### Table: invoices
Stores invoice details for reservations.

| Column Name     | Data Type | Constraints                                      | Description                              |
|-----------------|-----------|--------------------------------------------------|------------------------------------------|
| invoice_id      | INTEGER   | PRIMARY KEY AUTOINCREMENT                        | Unique identifier for the invoice        |
| reservation_id  | INTEGER   | NOT NULL FOREIGN KEY REFERENCES reservations(reservation_id) | ID of the associated reservation        |
| customer_id     | INTEGER   | NOT NULL FOREIGN KEY REFERENCES customers(customer_id) | ID of the customer for the invoice      |
| issue_date      | DATE      | NOT NULL                                         | Date the invoice was issued             |
| due_date        | DATE      | NOT NULL                                         | Date the invoice is due                 |
| total_amount    | REAL      | NOT NULL                                         | Total amount of the invoice             |
| status          | TEXT      | NOT NULL                                         | Invoice status (e.g., "Pending", "Paid") |
| created_at      | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP                        | Timestamp of record creation             |

**Relationships**:
- References `reservations.reservation_id` and `customers.customer_id` (foreign keys).
- Referenced by `payments.invoice_id` (foreign key).

#### Table: payments
Stores payment details for invoices.

| Column Name     | Data Type | Constraints                                      | Description                              |
|-----------------|-----------|--------------------------------------------------|------------------------------------------|
| payment_id      | INTEGER   | PRIMARY KEY AUTOINCREMENT                        | Unique identifier for the payment        |
| invoice_id      | INTEGER   | NOT NULL FOREIGN KEY REFERENCES invoices(invoice_id) | ID of the associated invoice            |
| customer_id     | INTEGER   | NOT NULL FOREIGN KEY REFERENCES customers(customer_id) | ID of the customer making the payment   |
| payment_date    | DATE      | NOT NULL                                         | Date of the payment                     |
| amount          | REAL      | NOT NULL                                         | Payment amount                          |
| payment_method  | TEXT      | NOT NULL                                         | Payment method (e.g., "Credit Card")     |
| created_at      | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP                        | Timestamp of record creation             |

**Relationships**:
- References `invoices.invoice_id` and `customers.customer_id` (foreign keys).

#### Table: facilities
Stores information about park facilities (e.g., restrooms, laundry rooms).

| Column Name     | Data Type | Constraints                                      | Description                              |
|-----------------|-----------|--------------------------------------------------|------------------------------------------|
| facility_id     | INTEGER   | PRIMARY KEY AUTOINCREMENT                        | Unique identifier for the facility       |
| facility_name   | TEXT      | NOT NULL                                         | Name of the facility (e.g., "Main Restroom") |
| facility_type   | TEXT      | NOT NULL                                         | Type of facility (e.g., "Restroom")       |
| location        | TEXT      |                                                  | Location of the facility (optional)       |
| is_active       | INTEGER   | NOT NULL DEFAULT 1                               | Facility availability (1 = active, 0 = inactive) |
| description     | TEXT      |                                                  | Optional description of the facility      |
| created_at      | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP                        | Timestamp of record creation             |

**Relationships**:
- Referenced by `assets.facility_id`, `maintenance_requests.facility_id`, `maintenance_schedules.facility_id`, and `maintenance_logs.facility_id` (foreign keys).

#### Table: assets
Tracks individual assets within facilities (e.g., a specific washer).

| Column Name     | Data Type | Constraints                                      | Description                              |
|-----------------|-----------|--------------------------------------------------|------------------------------------------|
| asset_id        | INTEGER   | PRIMARY KEY AUTOINCREMENT                        | Unique identifier for the asset          |
| facility_id     | INTEGER   | NOT NULL FOREIGN KEY REFERENCES facilities(facility_id) | ID of the associated facility           |
| asset_name      | TEXT      | NOT NULL                                         | Name of the asset (e.g., "Washer 1")     |
| asset_type      | TEXT      | NOT NULL                                         | Type of asset (e.g., "Washer")           |
| serial_number   | TEXT      |                                                  | Serial number of the asset (optional)    |
| purchase_date   | DATE      |                                                  | Purchase date of the asset (optional)    |
| is_active       | INTEGER   | NOT NULL DEFAULT 1                               | Asset availability (1 = active, 0 = inactive) |
| description     | TEXT      |                                                  | Optional description of the asset        |
| created_at      | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP                        | Timestamp of record creation             |

**Relationships**:
- References `facilities.facility_id` (foreign key).
- Referenced by `maintenance_requests.asset_id`, `maintenance_schedules.asset_id`, and `maintenance_logs.asset_id` (foreign keys).

#### Table: maintenance_requests
Records maintenance requests for facilities or assets.

| Column Name     | Data Type | Constraints                                      | Description                              |
|-----------------|-----------|--------------------------------------------------|------------------------------------------|
| request_id      | INTEGER   | PRIMARY KEY AUTOINCREMENT                        | Unique identifier for the request        |
| facility_id     | INTEGER   | FOREIGN KEY REFERENCES facilities(facility_id)   | ID of the associated facility (optional) |
| asset_id        | INTEGER   | FOREIGN KEY REFERENCES assets(asset_id)          | ID of the associated asset (optional)    |
| customer_id     | INTEGER   | FOREIGN KEY REFERENCES customers(customer_id)    | ID of the customer reporting the issue (optional) |
| request_date    | DATE      | NOT NULL                                         | Date the request was made                |
| priority        | TEXT      | NOT NULL                                         | Priority (e.g., "Low", "Medium", "High") |
| status          | TEXT      | NOT NULL                                         | Status (e.g., "Open", "In Progress", "Closed") |
| description     | TEXT      | NOT NULL                                         | Description of the maintenance issue     |
| created_at      | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP                        | Timestamp of record creation             |

**Constraints**:
- `CHECK (facility_id IS NOT NULL OR asset_id IS NOT NULL)`: Ensures at least one of `facility_id` or `asset_id` is provided.

**Relationships**:
- References `facilities.facility_id`, `assets.asset_id`, and `customers.customer_id` (foreign keys).
- Referenced by `maintenance_logs.request_id` (foreign key).

#### Table: maintenance_schedules
Manages scheduled maintenance tasks for facilities or assets.

| Column Name     | Data Type | Constraints                                      | Description                              |
|-----------------|-----------|--------------------------------------------------|------------------------------------------|
| schedule_id     | INTEGER   | PRIMARY KEY AUTOINCREMENT                        | Unique identifier for the schedule       |
| facility_id     | INTEGER   | FOREIGN KEY REFERENCES facilities(facility_id)   | ID of the associated facility (optional) |
| asset_id        | INTEGER   | FOREIGN KEY REFERENCES assets(asset_id)          | ID of the associated asset (optional)    |
| task_name       | TEXT      | NOT NULL                                         | Name of the maintenance task             |
| frequency       | TEXT      | NOT NULL                                         | Frequency (e.g., "Daily", "Weekly", "Monthly") |
| next_due_date   | DATE      | NOT NULL                                         | Next due date for the task               |
| status          | TEXT      | NOT NULL                                         | Status (e.g., "Pending", "Completed")    |
| description     | TEXT      |                                                  | Optional description of the task         |
| created_at      | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP                        | Timestamp of record creation             |

**Constraints**:
- `CHECK (facility_id IS NOT NULL OR asset_id IS NOT NULL)`: Ensures at least one of `facility_id` or `asset_id` is provided.

**Relationships**:
- References `facilities.facility_id` and `assets.asset_id` (foreign keys).
- Referenced by `maintenance_logs.schedule_id` (foreign key).

#### Table: maintenance_logs
Logs completed maintenance activities for auditing.

| Column Name     | Data Type | Constraints                                      | Description                              |
|-----------------|-----------|--------------------------------------------------|------------------------------------------|
| log_id          | INTEGER   | PRIMARY KEY AUTOINCREMENT                        | Unique identifier for the log entry      |
| requestim              | INTEGER   | FOREIGN KEY REFERENCES maintenance_requests(request_id) | ID of the associated maintenance request (optional) |
| schedule_id     | INTEGER   | FOREIGN KEY REFERENCES maintenance_schedules(schedule_id) | ID of the associated maintenance schedule (optional) |
| facility_id     | INTEGER   | FOREIGN KEY REFERENCES facilities(facility_id)   | ID of the associated facility (optional) |
| asset_id        | INTEGER   | FOREIGN KEY REFERENCES assets(asset_id)          | ID of the associated asset (optional)    |
| completion_date | DATE      | NOT NULL                                         | Date the maintenance was completed       |
| performed_by    | TEXT      | NOT NULL                                         | Name of the person who performed the maintenance |
| notes           | TEXT      |                                                  | Optional notes about the maintenance     |
| created_at      | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP                        | Timestamp of record creation             |

**Constraints**:
- `CHECK (facility_id IS NOT NULL OR asset_id IS NOT NULL)`: Ensures at least one of `facility_id` or `asset_id` is provided.

**Relationships**:
- References `maintenance_requests.request_id`, `maintenance_schedules.schedule_id`, `facilities.facility_id`, and `assets.asset_id` (foreign keys).

## Notes
- The schema is designed for SQLite and uses `INTEGER` for primary keys with `AUTOINCREMENT` to ensure unique IDs.
- Foreign keys enforce referential integrity between tables (e.g., a reservation must reference a valid customer and RV site).
- The `created_at` timestamp in each table provides an audit trail for record creation.
- The `reservations` table includes a `CHECK` constraint to ensure logical date ranges.
- The `rv_sites.is_active`, `facilities.is_active`, and `assets.is_active` fields allow for soft deletion (marking records inactive without removing them).
- The maintenance tables include `CHECK` constraints to ensure maintenance requests, schedules, and logs target either a facility or an asset.
- The schema matches the implementation in `InitializeSQLiteDatabase.py`, `maintenance/InitializeMaintenanceDatabase.py`, and `crm/test咖啡_components.py` as of the current project state.

## Troubleshooting
- **Database Errors**:
  - If `no such table` errors occur, ensure both `InitializeSQLiteDatabase.py` and `maintenance/InitializeMaintenanceDatabase.py` have been run, or check `crm/test_crm_components.py` for schema issues.
  - Verify `park.db` or `test_park.db` is writable:
    ```bash
    ls -l .
    ```
- **Test Failures**:
  - Run tests with verbose output to identify failing tests:
    ```bash
    python crm/test_crm_components.py -v
    ```
  - Check `crm_errors.log` for logged errors.
- **Permissions**:
  - Ensure write permissions for `park.db`, `test_park.db`, and `crm_errors.log`.
- **Slow Tests**:
  - Check disk performance:
    ```bash
    df -h .
    ```
  - Consider modifying `crm/test_crm_components.py` to reuse the test database by clearing tables instead of deleting the file.

## .gitignore Configuration
The `.gitignore` file excludes files and directories to keep the repository clean. Key exclusions include:
- Python bytecode: `__pycache__/, *.pyc, *.pyo, *.pyd`
- Virtual environments: `venv/, env/, .env/, .venv/`
- Database files: `*.db` (e.g., `park.db`, `test_park.db`)
- Logs: `crm_errors.log`
- IDE files: `.idea/, .vscode/`
- Build artifacts: `dist/, build/, *.egg-info/`
- Testing artifacts: `.coverage, coverage.xml, pytest_cache/`

Modify `.gitignore` for project-specific needs, ensuring sensitive data is excluded.

## Future Improvements
- Add a frontend interface for user interaction.
- Implementformerly, implement additional maintenance module components (e.g., `MaintenanceDatabase.py`, `MaintenanceService.py`, `MaintenanceValidator.py`, `MaintenanceErrorHandler.py`, `test_maintenance_components.py`).
- Implement additional features like cancellation policies or reporting.
- Optimize test performance for large datasets.
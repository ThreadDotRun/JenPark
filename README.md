


## InitializeSQLiteDatabase Component

### Overview
The `InitializeSQLiteDatabase.py` component is responsible for setting up the SQLite database (`park.db`) for the RV Park CRM/ERP system. It creates the necessary tables (`customers`, `rv_sites`, `reservations`, `invoices`, and `payments`) with appropriate schema, including foreign keys and constraints, if they do not already exist.

### Features
- Creates a SQLite database file (`park.db`) if it doesn't exist.
- Defines tables with `CREATE TABLE IF NOT EXISTS` to prevent overwriting existing data.
- Includes error handling for database connection and table creation.
- Automatically closes database connections to avoid resource leaks.
- Supports the core data structure for managing customers, RV sites, reservations, invoices, and payments.

### Requirements
- Python 3.6 or higher
- SQLite3 (included with Python standard library)

### Usage
1. Ensure Python is installed on your system.
2. Save `InitializeSQLiteDatabase.py` in your project directory.
3. Run the script directly to initialize the database:
   ```bash
   python InitializeSQLiteDatabase.py
   ```
4. Alternatively, import and use the class in your application:
   ```python
   from InitializeSQLiteDatabase import InitializeSQLiteDatabase

   db_initializer = InitializeSQLiteDatabase()
   db_initializer.initialize()
   ```

### Output
- Creates a `park.db` file in the project directory.
- Prints status messages indicating successful connection, table creation, and connection closure, or error messages if issues occur.

### Notes
- The database schema is designed to support RV park operations, with tables linked via foreign keys for data integrity.
- This component is idempotent; running it multiple times will not duplicate tables or cause errors.
- Ensure write permissions in the project directory to create the `park.db` file.

## .gitignore Configuration

The `.gitignore` file is configured to exclude files and directories that should not be tracked by Git, ensuring a clean repository. It includes common Python-related exclusions to prevent unnecessary or sensitive files from being committed.

### Key Exclusions
- **Python Bytecode and Cache**: Ignores `__pycache__/`, `*.pyc`, `*.pyo`, and `*.pyd` files generated during code execution.
- **Virtual Environments**: Excludes `venv/`, `env/`, `.env/`, and `.venv/` to keep environment-specific configurations local.
- **IDE/Editor Files**: Ignores `.idea/`, `.vscode/`, and Sublime Text project files to avoid committing editor-specific settings.
- **OS Files**: Excludes `.DS_Store` (macOS) and `Thumbs.db` (Windows) to prevent operating system artifacts.
- **Build Artifacts**: Ignores `dist/`, `build/`, and `*.egg-info/` directories created during packaging.
- **Testing and Coverage**: Excludes `.coverage`, `coverage.xml`, and `pytest_cache/` to keep test-related files out of the repository.
- **Jupyter Notebooks**: Ignores `.ipynb_checkpoints/` for clean notebook version control.
- **Environment Variables**: Excludes `.env` and `.env.local` to protect sensitive configuration data.

### Customization
Modify the `.gitignore` file to include project-specific files or directories as needed. Ensure sensitive data, such as API keys or credentials, is added to the exclusions.

For the full `.gitignore` content, see [`.gitignore`](./.gitignore).
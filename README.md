# OVA POS

OVA POS is a desktop point-of-sale application built with Python and PyQt6. It includes cashier workflows, product and barcode management, invoice handling, and user access for admin and cashier roles.

## Features

- User login screen
- Admin dashboard for management operations
- Cashier interface for sales
- Product management and barcode support
- Invoice and invoice-item tracking
- SQLite database layer with migration files
- Printer integration support

## Project structure

- `main.py` — application entry point
- `Interface/` — GUI windows and widgets
- `Model/` — database models and data access classes
- `DB/` — SQLite database and migration scripts
- `Utils/` — helper utilities
- `build/` — generated PyInstaller build output
- `main.spec` — packaging configuration for PyInstaller

## Requirements

- Python 3.10+
- PyQt6
- SQLite3 (included with Python)

## Setup

1. Open a terminal in the project folder.
2. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

3. Activate it:

   - Windows:

     ```bash
     .venv\Scripts\activate
     ```

   - Linux/macOS:

     ```bash
     source .venv/bin/activate
     ```

4. Install dependencies:

   ```bash
   pip install PyQt6
   ```

## Run the app

```bash
python main.py
```

## Database setup

The project uses SQLite and includes migration scripts under `DB/Migration`.

To create or update the database structure, run:

```bash
python Migrate.py
```

The database file is stored at:

```text
DB/DataBase.sqlite
```

This database is intentionally kept in the repository so the app can run with the default data already available.

## Default admin account

- Name: `Admin`
- Password: `Admin`

You can also seed the default admin user manually with:

```bash
python Seeed.py
```

## Build executable

If you want to package the app with PyInstaller:

```bash
pyinstaller main.spec
```

## Notes

- The project is designed for local desktop usage.
- Generated build files are ignored by Git via the root `.gitignore`.
- The SQLite database file remains tracked in the repository for the default app setup.
- Default admin login:
  - Name: `Admin`
  - Password: `Admin`

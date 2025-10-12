# Record Management System

This project is a simple record management system for a travel agent, handling Client, Airline, and Flight records via a GUI. Records are stored as a list of dictionaries in memory and persisted to JSON.

## Project Structure
- `src/main.py`: GUI and main app logic.
- `src/storage.py`: File load/save functions for records.
- `src/records.py`: CRUD functions for managing records.
- `tests/`: Unit tests (e.g., test_storage.py for storage module).
- `records.json`: Data file (ignored in Git).

## Storage Module (src/storage.py)
Handles persistence of records using JSON.
- Load records: `records = load_records('../records.json')` (returns list of dicts or empty if not found).
- Save records: `save_records(records, '../records.json')`.
- Paths are relative; adjust as needed from caller.

## Running Tests
Install pytest: `pip install pytest` (in venv).
Run: `pytest tests/test_storage.py` (or python -m pytest tests/test_storage.py if PATH issues occur; requires pytest installed in venv). (verifies load/save for storage module).
Run: `pytest tests/test_records.py` (or python -m pytest tests/test_records.py if PATH issues occur; requires pytest installed in venv). (verifies load/save for storage module).

## Setup
1. Activate venv: `.venv\Scripts\activate.bat` (cmd).
2. Install requirements: `pip install -r requirements.txt`.
3. Run app: `python src/main.py`.
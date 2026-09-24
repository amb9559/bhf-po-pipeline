# bhf-po-pipeline
Parses semi-structured vendor purchase orders (multiple layouts) into validated, template-matched Excel output, flags data issues explicitly, and loads results idempotently into SQLite with audit logging.

## Project structure

- `app/` - application entry points
- `parsers/` - layout-specific parsing modules
- `models/` - normalized data models and validation helpers
- `outputs/` - Excel and SQLite output handlers
- `tests/` - parser, validation, and idempotency tests

## Active branch

- `feature/po-pipeline`

## Input data

The project reads source PO text files from the dedicated `input_data/` directory.

## Step 1: parser and input ingestion

Completed and verified.

- Added a layout detector that identifies fixed-width vs key/value PO layouts.
- Implemented a fixed-width parser for table-based purchase orders.
- Implemented a key/value parser for label-based purchase orders.
- Added a file loader that reads all text files from `input_data/`.
- Added parser and input-loading tests.

### Verification

The Step 1 test suite passed with fresh evidence:

- `C:/Users/ambuj/AppData/Local/Python/pythoncore-3.14-64/python.exe -m pytest -q tests/test_layout_detector.py tests/test_input_loader.py`
- Result: `5 passed in 0.08s`

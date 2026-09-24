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

The project reads source PO text files from the `Data_Engineer_Take_Home_Assignment/` directory.

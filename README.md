# bhf-po-pipeline

This project reads purchase order text files, extracts the data in a consistent format, checks the quality of each record, and prepares the cleaned result for Excel and SQLite output.

## Project structure

- `app/` - pipeline entry points
- `parsers/` - logic for each PO file layout
- `models/` - PO data models and validation rules
- `outputs/` - Excel export and SQLite loading
- `tests/` - automated checks for parsing, validation, and output
- `input_data/` - raw purchase order source files

## Current branch

- `feature/po-pipeline`

## Current step progress

### Step 1: parsing and file loading

We added the first working pieces of the pipeline:

- a detector to recognize fixed-width and key/value purchase order layouts
- a parser for the table-style PO format
- a parser for the label-based PO format
- a loader that reads all files from `input_data/`
- tests to confirm the parsing logic is working correctly

### Step 2: validation checks

We added the validation layer so the pipeline can flag bad purchase order records before they are exported:

- required field checks for header data and line items
- duplicate PO number detection
- invalid value checks for UPC, department, negatives, and zero-value fields
- arithmetic checks for ext qty and ext cost
- basic referential integrity checks for item-level consistency

### Step 3: output generation

We are now building the export layer so cleaned PO records can be written out in a usable format:

- Excel export for the processed data
- SQLite load for storing normalized records
- validation tests for the output layer

## How to run the project

From the project root, you can run the test suite with:

```bash
python -m pytest -q
```

The input data is expected in the `input_data/` folder.


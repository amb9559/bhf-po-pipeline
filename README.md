# bhf-po-pipeline

This project reads vendor purchase order text files, parses the different formats, validates the data, and prepares it for Excel and SQLite output.

## Project layout

- `app/` - entry points for the pipeline
- `parsers/` - code for reading and extracting data from each PO layout
- `models/` - data models and validation helpers
- `outputs/` - Excel and SQLite output logic
- `tests/` - checks for parsing and ingestion

## Current branch

- `feature/po-pipeline`

## Input files

The raw purchase order files are kept in `input_data/`.

## Step 1: parsing and file loading

This step is complete.

We added the first working pieces of the pipeline:

- a detector to recognize the fixed-width and key/value PO formats
- a parser for the table-style purchase order layout
- a parser for the label-based purchase order layout
- a loader that reads all input files from `input_data/`
- tests to confirm the detection and parsing work correctly

## Step 2: validation checks

This step is also complete.

We added the validation layer so the pipeline can flag bad purchase orders before they are exported:

- required field checks for header and line item data
- ext qty validation against cartons and case pack values
- ext cost validation against quantity and unit cost
- issue tracking on each parsed PO record
- tests covering valid records, missing required values, and arithmetic mismatches


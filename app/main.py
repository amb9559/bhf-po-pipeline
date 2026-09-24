"""Entry point for the purchase-order parsing pipeline."""

from pathlib import Path

from models.po_models import POHeader, POLineItem, PORecord
from models.validation import validate_record
from outputs.excel_writer import write_excel
from outputs.sqlite_loader import load_to_sqlite
from parsers.fixed_width_parser import parse_fixed_width
from parsers.key_value_parser import parse_key_value
from parsers.layout_detector import detect_layout
from parsers.loader import load_po_files


def _build_record(parsed_text, layout):
    """Convert parsed raw dictionary output into normalized PORecord objects."""
    header_data = parsed_text.get("header", {})
    header = POHeader(
        po_number=header_data.get("po_number"),
        vendor_name=header_data.get("vendor_name"),
        buyer=header_data.get("buyer"),
        ship_date=header_data.get("ship_date"),
        ship_terms=header_data.get("ship_terms"),
        ref_po=header_data.get("ref_po"),
    )

    line_items = []
    for item_data in parsed_text.get("line_items", []):
        item = POLineItem(
            sku=item_data.get("sku"),
            upc=item_data.get("upc"),
            department=item_data.get("department") or item_data.get("dept"),
            vendor_part=item_data.get("vendor_part"),
            description=item_data.get("description"),
            retail=item_data.get("retail"),
            cost=item_data.get("cost"),
            cartons=item_data.get("cartons"),
            case_pack=item_data.get("case_pack"),
            ext_qty=item_data.get("ext_qty"),
            ext_cost=item_data.get("ext_cost"),
            cube=item_data.get("cube"),
            kilograms=item_data.get("kg"),
        )
        line_items.append(item)

    record = PORecord(header=header, line_items=line_items)
    if layout == "fixed_width":
        record.source_file = "fixed_width"
    else:
        record.source_file = "key_value"
    return record


def run_pipeline(input_dir="input_data", output_dir="output", db_path="output/purchase_orders.db"):
    """Run the full purchase order processing pipeline."""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    db_file = Path(db_path)

    files = load_po_files(input_path)
    records = []
    seen_po_numbers = set()

    for text in files:
        layout = detect_layout(text)
        if layout == "fixed_width":
            parsed = parse_fixed_width(text)
        else:
            parsed = parse_key_value(text)

        record = _build_record(parsed, layout)
        record = validate_record(record, seen_po_numbers=seen_po_numbers)
        records.append(record)
        if record.header.po_number:
            seen_po_numbers.add(str(record.header.po_number).strip())

    excel_path = output_path / "purchase_orders.xlsx"
    write_excel(records, excel_path)
    load_to_sqlite(records, db_file)
    return records


def main() -> None:
    """Run the end-to-end purchase order pipeline."""
    project_root = Path(__file__).resolve().parent.parent
    input_dir = project_root / "input_data"
    output_dir = project_root / "output"
    db_path = output_dir / "purchase_orders.db"

    records = run_pipeline(input_dir=input_dir, output_dir=output_dir, db_path=db_path)
    print(f"Processed {len(records)} purchase order records.")
    print(f"Excel file: {output_dir / 'purchase_orders.xlsx'}")
    print(f"SQLite database: {db_path}")


if __name__ == "__main__":
    main()

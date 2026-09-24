"""Tests for Excel and SQLite output layers."""

import sqlite3

from openpyxl import load_workbook

from models.po_models import POHeader, POLineItem, PORecord
from outputs.excel_writer import write_excel
from outputs.sqlite_loader import load_to_sqlite


def test_write_excel_creates_file(tmp_path):
    output_path = tmp_path / "po_output.xlsx"
    records = [
        PORecord(
            header=POHeader(po_number="PO-100", vendor_name="Vendor A", buyer="Buyer 1"),
            line_items=[
                POLineItem(
                    sku="SKU-1",
                    upc="123456789012",
                    department="210",
                    vendor_part="VP-1",
                    description="Widget",
                    retail=29.99,
                    cost=12.50,
                    cartons=3,
                    case_pack=4,
                    ext_qty=12,
                    ext_cost=150.00,
                    cube=0.20,
                    kilograms=2.5,
                )
            ],
        )
    ]

    result = write_excel(records, output_path)

    assert result == output_path
    assert output_path.exists()

    workbook = load_workbook(output_path)
    sheet = workbook.active
    assert sheet["A1"].value == "po_number"
    assert sheet["B1"].value == "vendor_name"
    assert sheet["A2"].value == "PO-100"
    assert sheet["B2"].value == "Vendor A"


def test_load_to_sqlite_creates_table_and_rows(tmp_path):
    db_path = tmp_path / "po_database.db"
    records = [
        PORecord(
            header=POHeader(po_number="PO-200", vendor_name="Vendor B", buyer="Buyer 2"),
            line_items=[
                POLineItem(
                    sku="SKU-2",
                    upc="123456789013",
                    department="220",
                    vendor_part="VP-2",
                    description="Gadget",
                    retail=99.99,
                    cost=45.00,
                    cartons=2,
                    case_pack=5,
                    ext_qty=10,
                    ext_cost=450.00,
                    cube=0.50,
                    kilograms=4.0,
                )
            ],
        )
    ]

    result = load_to_sqlite(records, db_path)

    assert result == db_path
    assert db_path.exists()

    connection = sqlite3.connect(db_path)
    rows = connection.execute(
        "SELECT po_number, vendor_name, buyer FROM purchase_orders ORDER BY po_number"
    ).fetchall()
    connection.close()

    assert rows == [("PO-200", "Vendor B", "Buyer 2")]

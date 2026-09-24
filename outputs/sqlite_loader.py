"""SQLite loader for normalized PO data."""

import sqlite3


def load_to_sqlite(records, db_path):
    """Write PO records to a SQLite database."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS purchase_orders (
            po_number TEXT,
            vendor_name TEXT,
            buyer TEXT,
            sku TEXT,
            upc TEXT,
            department TEXT,
            vendor_part TEXT,
            description TEXT,
            retail REAL,
            cost REAL,
            cartons INTEGER,
            case_pack INTEGER,
            ext_qty INTEGER,
            ext_cost REAL,
            cube REAL,
            kilograms REAL
        )
        """
    )

    for record in records:
        header = record.header
        for item in record.line_items:
            cursor.execute(
                """
                INSERT INTO purchase_orders (
                    po_number, vendor_name, buyer, sku, upc, department, vendor_part,
                    description, retail, cost, cartons, case_pack, ext_qty, ext_cost,
                    cube, kilograms
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    getattr(header, "po_number", None),
                    getattr(header, "vendor_name", None),
                    getattr(header, "buyer", None),
                    getattr(item, "sku", None),
                    getattr(item, "upc", None),
                    getattr(item, "department", None),
                    getattr(item, "vendor_part", None),
                    getattr(item, "description", None),
                    getattr(item, "retail", None),
                    getattr(item, "cost", None),
                    getattr(item, "cartons", None),
                    getattr(item, "case_pack", None),
                    getattr(item, "ext_qty", None),
                    getattr(item, "ext_cost", None),
                    getattr(item, "cube", None),
                    getattr(item, "kilograms", None),
                ),
            )

    connection.commit()
    connection.close()
    return db_path

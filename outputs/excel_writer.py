"""Excel output writer for normalized PO records."""

from openpyxl import Workbook


def write_excel(records, output_path):
    """Write PO records to an Excel workbook."""
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "purchase_orders"

    headers = [
        "po_number",
        "vendor_name",
        "buyer",
        "sku",
        "upc",
        "department",
        "vendor_part",
        "description",
        "retail",
        "cost",
        "cartons",
        "case_pack",
        "ext_qty",
        "ext_cost",
        "cube",
        "kilograms",
    ]
    sheet.append(headers)

    for record in records:
        header = record.header
        for item in record.line_items:
            row = [
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
            ]
            sheet.append(row)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    workbook.save(output_path)
    return output_path

"""Parser for key/value purchase-order layout."""

import re


def parse_key_value(text: str):
    """Extract header and items from the key:value PO layout."""
    lines = [line.rstrip() for line in text.splitlines()]
    header = {}
    line_items = []
    current_item = {}

    for line in lines:
        if "PO NUMBER" in line and ":" in line:
            header["po_number"] = re.split(r":\s*", line, maxsplit=1)[1].strip()
        elif "VENDOR NAME" in line and ":" in line:
            header["vendor_name"] = re.split(r":\s*", line, maxsplit=1)[1].strip()
        elif "BUYER" in line and ":" in line:
            header["buyer"] = re.split(r":\s*", line, maxsplit=1)[1].strip()
        elif "SHIP DATE" in line and ":" in line:
            header["ship_date"] = re.split(r":\s*", line, maxsplit=1)[1].strip()
        elif "SHIP TERMS" in line and ":" in line:
            header["ship_terms"] = re.split(r":\s*", line, maxsplit=1)[1].strip()

        if line.startswith("SKU:"):
            if current_item:
                line_items.append(current_item)
            current_item = {}
            match = re.search(r"SKU:\s*(\S+)\s+UPC:\s*(\S+)\s+DEPT:\s*(\d+)", line)
            if match:
                current_item["sku"] = match.group(1)
                current_item["upc"] = match.group(2)
                current_item["department"] = match.group(3)

        elif line.startswith("DESC:"):
            current_item["description"] = line.split("DESC:", 1)[1].strip()

        elif re.match(r"^\s*RETAIL:\s*", line):
            current_item["retail"] = re.split(r":\s*", line, maxsplit=1)[1].strip()

        elif re.match(r"^\s*COST:\s*", line):
            current_item["cost"] = re.split(r":\s*", line, maxsplit=1)[1].strip()

        elif re.match(r"^\s*CARTONS:\s*", line):
            current_item["cartons"] = re.split(r":\s*", line, maxsplit=1)[1].strip()

        elif re.match(r"^\s*CASE PACK:\s*", line):
            current_item["case_pack"] = re.split(r":\s*", line, maxsplit=1)[1].strip()

        elif re.match(r"^\s*EXT QTY:\s*", line):
            current_item["ext_qty"] = re.split(r":\s*", line, maxsplit=1)[1].strip()

        elif re.match(r"^\s*EXT COST:\s*", line):
            current_item["ext_cost"] = re.split(r":\s*", line, maxsplit=1)[1].strip()

        elif re.match(r"^\s*CUBE:\s*", line):
            current_item["cube"] = re.split(r":\s*", line, maxsplit=1)[1].strip()

        elif re.match(r"^\s*KG:\s*", line):
            current_item["kg"] = re.split(r":\s*", line, maxsplit=1)[1].strip()

    if current_item:
        line_items.append(current_item)

    return {"raw_text": text, "layout": "key_value", "header": header, "line_items": line_items}

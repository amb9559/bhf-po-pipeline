"""Parser for fixed-width purchase-order layout."""

import re


def parse_fixed_width(text: str):
    """Extract header and items from the fixed-width PO layout."""
    lines = [line.rstrip() for line in text.splitlines()]
    header = {}
    line_items = []
    totals = {}

    for line in lines:
        if "BUYER:" in line:
            header["buyer"] = line.split("BUYER:", 1)[1].strip()
        elif "SHIP TERMS:" in line:
            header["ship_terms"] = line.split("SHIP TERMS:", 1)[1].split("PURCHASE ORDER", 1)[0].strip()
        elif "PO#:" in line:
            header["po_number"] = line.split("PO#:", 1)[1].strip()
        elif "REF MASTER PO#:" in line:
            header["ref_po"] = line.split("REF MASTER PO#:", 1)[1].strip()
        elif "SHIP DATE:" in line:
            header["ship_date"] = line.split("SHIP DATE:", 1)[1].strip()
        elif "TOTALS:" in line:
            totals_match = re.search(r"TOTALS:\s*(.*)", line)
            if totals_match:
                totals["raw"] = totals_match.group(1).strip()
                totals["ext_cost"] = totals_match.group(1).split()[0].strip() if totals_match.group(1).split() else ""

        if re.match(r"^\s*\d+\s+\S+", line):
            match = re.match(r"^\s*(\d+)\s+(\S+)\s+(\S+)\s{2,}(.*)$", line.strip())
            if match:
                item = {
                    "dept": match.group(1),
                    "sku": match.group(2),
                    "vendor_part": match.group(3),
                    "description": match.group(4).strip(),
                }
                line_items.append(item)

    return {"raw_text": text, "layout": "fixed_width", "header": header, "line_items": line_items, "totals": totals}

"""Validation helpers for PO records."""


def _as_float(value):
    """Safely convert values to float."""
    if value in (None, ""):
        return None
    try:
        return float(str(value).replace(",", ""))
    except (TypeError, ValueError):
        return None


def _as_int(value):
    """Safely convert values to int."""
    if value in (None, ""):
        return None
    try:
        return int(str(value).replace(",", ""))
    except (TypeError, ValueError):
        return None


def _is_digits(value):
    """Return true when the value is a numeric string."""
    if value is None:
        return False
    text = str(value).strip()
    return bool(text) and text.isdigit()


def validate_record(record, seen_po_numbers=None):
    """Validate required PO data, duplicate keys, invalid values, and arithmetic checks."""
    issues = list(record.issues)
    seen_po_numbers = set(seen_po_numbers or set())

    required_header_fields = [
        ("po_number", "PO number"),
        ("vendor_name", "vendor name"),
        ("buyer", "buyer"),
    ]

    po_number = getattr(record.header, "po_number", None)
    if po_number is not None and str(po_number).strip():
        normalized_po = str(po_number).strip()
        if normalized_po in seen_po_numbers:
            issues.append(f"duplicate PO number: {normalized_po}")
        seen_po_numbers.add(normalized_po)
    else:
        issues.append("missing required header field: PO number")

    for field_name, label in required_header_fields:
        value = getattr(record.header, field_name, None)
        if value is None or str(value).strip() == "":
            issues.append(f"missing required header field: {label}")

    for index, item in enumerate(record.line_items, start=1):
        if not item.sku or not item.upc or not item.description:
            issues.append(f"line item {index}: missing required item fields")

        if item.upc is not None and str(item.upc).strip() and (not str(item.upc).strip().isdigit() or len(str(item.upc).strip()) != 12):
            issues.append(f"line item {index}: invalid UPC value")

        if item.department is not None and str(item.department).strip() and not _is_digits(item.department):
            issues.append(f"line item {index}: invalid department code")

        numeric_checks = [
            (item.retail, "retail"),
            (item.cost, "cost"),
            (item.cartons, "cartons"),
            (item.case_pack, "case pack"),
            (item.ext_qty, "ext qty"),
            (item.ext_cost, "ext cost"),
            (item.cube, "cube"),
            (item.kilograms, "kilograms"),
        ]

        for value, label in numeric_checks:
            if value is None:
                continue
            numeric_value = _as_float(value) if label not in {"cartons", "case pack", "ext qty"} else _as_int(value)
            if numeric_value is None:
                issues.append(f"line item {index}: invalid {label} value")
                continue
            if numeric_value < 0:
                issues.append(f"line item {index}: invalid {label} value")
            elif label in {"cost", "ext cost", "retail", "cube", "kilograms"} and numeric_value <= 0:
                issues.append(f"line item {index}: invalid {label} value")
            elif label in {"cartons", "case pack", "ext qty"} and numeric_value <= 0:
                issues.append(f"line item {index}: invalid {label} value")

        if item.case_pack is not None and item.cartons is not None and item.case_pack > 0 and item.cartons > 0:
            expected_qty = item.case_pack * item.cartons
            if item.ext_qty is not None and item.ext_qty != expected_qty:
                issues.append(f"line item {index}: ext qty mismatch (expected {expected_qty}, found {item.ext_qty})")

        if item.cost is not None and item.ext_qty is not None and item.ext_cost is not None:
            expected_ext_cost = _as_float(item.cost) * _as_int(item.ext_qty)
            actual_ext_cost = _as_float(item.ext_cost)
            if expected_ext_cost is not None and actual_ext_cost is not None and abs(expected_ext_cost - actual_ext_cost) > 0.01:
                issues.append(f"line item {index}: ext cost mismatch (expected {expected_ext_cost}, found {actual_ext_cost})")

        if item.upc is not None and str(item.upc).strip() and not item.sku:
            issues.append(f"line item {index}: referential integrity issue: UPC provided without SKU")

    record.issues = issues
    return record

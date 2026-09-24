"""Tests for validation rules on parsed PO data."""

from models.po_models import POHeader, POLineItem, PORecord
from models.validation import validate_record


def test_valid_record_passes_validation():
    record = PORecord(
        header=POHeader(po_number="PO-100", vendor_name="Test Vendor", buyer="Test Buyer"),
        line_items=[
            POLineItem(
                sku="123",
                upc="123456789012",
                department="210",
                vendor_part="ABC-1",
                description="Test item",
                retail=29.99,
                cost=10.00,
                cartons=2,
                case_pack=4,
                ext_qty=8,
                ext_cost=80.00,
                cube=0.10,
                kilograms=1.5,
            )
        ],
    )

    validated = validate_record(record)
    assert validated.issues == []


def test_missing_required_fields_are_flagged():
    record = PORecord(
        header=POHeader(po_number="", vendor_name="", buyer=""),
        line_items=[POLineItem(sku="", upc="", description="")],
    )

    validated = validate_record(record)
    assert any("missing required" in issue.lower() for issue in validated.issues)


def test_math_mismatch_is_flagged():
    record = PORecord(
        header=POHeader(po_number="PO-100", vendor_name="Vendor", buyer="Buyer"),
        line_items=[
            POLineItem(
                sku="123",
                upc="123456789012",
                department="210",
                vendor_part="ABC-1",
                description="Test item",
                retail=29.99,
                cost=10.00,
                cartons=2,
                case_pack=4,
                ext_qty=8,
                ext_cost=50.00,
                cube=0.10,
                kilograms=1.5,
            )
        ],
    )

    validated = validate_record(record)
    assert any("ext cost" in issue.lower() for issue in validated.issues)


def test_duplicate_po_number_is_flagged():
    record = PORecord(
        header=POHeader(po_number="PO-100", vendor_name="Vendor", buyer="Buyer"),
        line_items=[],
    )

    validated = validate_record(record, seen_po_numbers={"PO-100"})
    assert any("duplicate po number" in issue.lower() for issue in validated.issues)


def test_invalid_values_and_referential_integrity_are_flagged():
    record = PORecord(
        header=POHeader(po_number="PO-200", vendor_name="Vendor", buyer="Buyer"),
        line_items=[
            POLineItem(
                sku="",
                upc="ABC",
                department="XYZ",
                vendor_part="ABC-1",
                description="Bad item",
                retail=-1,
                cost=0,
                cartons=0,
                case_pack=0,
                ext_qty=-5,
                ext_cost=-10,
                cube=-0.1,
                kilograms=-1.0,
            )
        ],
    )

    validated = validate_record(record)
    assert any("invalid" in issue.lower() for issue in validated.issues)
    assert any("upc" in issue.lower() or "department" in issue.lower() for issue in validated.issues)

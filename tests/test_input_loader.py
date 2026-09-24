"""Tests for loading purchase-order text files."""

from pathlib import Path

from parsers.fixed_width_parser import parse_fixed_width
from parsers.key_value_parser import parse_key_value


ROOT = Path(__file__).resolve().parents[1]
INPUT_DIR = ROOT / "input_data"


def test_fixed_width_parser_extracts_header_and_rows():
    text = ("BUYER: 610 JORDAN MILLER\n"
            "SHIP TERMS: FOB Ningbo,CHN\n"
            "DPT SKU/UPC       VENDOR PART#  DESCRIPTION\n"
            "210 71097188      04212         NORDPEAK ASHER T CMFST GRY\n"
            "TOTALS: 447455.120  3475\n")

    result = parse_fixed_width(text)
    assert result["layout"] == "fixed_width"
    assert result["header"]["buyer"] == "610 JORDAN MILLER"
    assert len(result["line_items"]) >= 1
    assert result["totals"]["ext_cost"] == "447455.120"


def test_key_value_parser_extracts_key_value_fields():
    text = ("PURCHASE ORDER\n"
            "PO NUMBER   : PL7M3RK\n"
            "VENDOR NAME : CRESTLINE MFG CO LTD\n"
            "LINE ITEM DETAIL\n"
            "SKU: 88304410   UPC: 0071230441087   DEPT: 340\n"
            "DESC: HARLOW QUILT SET T WHT\n")

    result = parse_key_value(text)
    assert result["layout"] == "key_value"
    assert result["header"]["po_number"] == "PL7M3RK"
    assert result["line_items"][0]["sku"] == "88304410"


def test_input_files_exist_in_input_data_folder():
    files = sorted(p.name for p in INPUT_DIR.glob("*.txt"))
    assert "purchase_order_sample.txt" in files
    assert "purchase_order_sample_2.txt" in files

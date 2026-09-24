"""Tests for layout detection."""

from parsers.layout_detector import detect_layout


def test_fixed_width_layout_detected():
    text = "DPT SKU/UPC       VENDOR PART#  DESCRIPTION\nTOTALS: 123"
    assert detect_layout(text) == "fixed_width"


def test_key_value_layout_detected():
    text = "LINE ITEM DETAIL\nSKU: 88304410   UPC: 0071230441087"
    assert detect_layout(text) == "key_value"

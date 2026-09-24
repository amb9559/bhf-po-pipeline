"""Detect the layout format of a purchase-order text file."""


def detect_layout(text: str) -> str:
    """Return the layout type based on file markers."""
    if "LINE ITEM DETAIL" in text or "SKU:" in text:
        return "key_value"
    if "DPT SKU/UPC" in text or "TOTALS:" in text:
        return "fixed_width"
    raise ValueError("Unsupported purchase-order layout")

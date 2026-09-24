"""Input loader for source purchase-order text files."""

from pathlib import Path


def load_po_files(input_dir: str | Path):
    """Load all raw purchase-order text files from the given directory."""
    input_path = Path(input_dir)
    if not input_path.exists():
        raise FileNotFoundError(f"Input directory not found: {input_path}")

    files = sorted(input_path.glob("*.txt"))
    return [file.read_text(encoding="utf-8", errors="replace") for file in files]

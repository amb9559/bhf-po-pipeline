"""End-to-end pipeline tests."""

from app.main import run_pipeline


def test_run_pipeline_processes_input_files(tmp_path):
    input_dir = tmp_path / "input_data"
    input_dir.mkdir()

    sample_file = input_dir / "sample_po.txt"
    sample_file.write_text(
        """
PO NUMBER : PO-400
VENDOR NAME : Vendor A
BUYER : Buyer 1
SKU: ABC-1 UPC: 123456789012 DEPT: 210
DESC: Test item
RETAIL: 29.99
COST: 10.00
CARTONS: 2
CASE PACK: 4
EXT QTY: 8
EXT COST: 80.00
CUBE: 0.10
KG: 1.50
""".strip(),
        encoding="utf-8",
    )

    output_dir = tmp_path / "output"
    db_path = output_dir / "purchase_orders.db"
    excel_path = output_dir / "purchase_orders.xlsx"

    records = run_pipeline(input_dir=input_dir, output_dir=output_dir, db_path=db_path)

    assert len(records) == 1
    assert records[0].header.po_number == "PO-400"
    assert excel_path.exists()
    assert db_path.exists()

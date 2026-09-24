"""Entry point for the purchase-order parsing pipeline."""

from pathlib import Path


def main() -> None:
    """Main entry point placeholder for the processing pipeline."""
    input_dir = Path(__file__).resolve().parent.parent / "Data_Engineer_Take_Home_Assignment"
    print(f"Input directory: {input_dir}")


if __name__ == "__main__":
    main()

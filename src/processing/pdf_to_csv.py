from pathlib import Path
import argparse
import os
import sys
from typing import List

try:
    import pdfplumber
    import pandas as pd
except ImportError as e:
    print("Missing required package: {}".format(e.name if hasattr(e, 'name') else e))
    print("Please install requirements: pip install -r requirements.txt")
    sys.exit(1)


def find_pdfs(pdf_dir: Path, recursive: bool = False) -> List[Path]:
    if recursive:
        return sorted(pdf_dir.rglob("*.pdf"))
    return sorted(pdf_dir.glob("*.pdf"))


def extract_tables_from_pdf(pdf_path: Path, out_dir: Path) -> int:
    """Extract tables from a single PDF and write CSVs to out_dir.

    Returns the number of tables written.
    """
    tables_written = 0
    try:
        with pdfplumber.open(str(pdf_path)) as pdf:
            for page_idx, page in enumerate(pdf.pages):
                # pdfplumber's extract_tables returns a list of tables (list of rows)
                try:
                    page_tables = page.extract_tables()
                except Exception as e:
                    print(f"Warning: failed to extract tables from {pdf_path.name} page {page_idx+1}: {e}")
                    continue

                if not page_tables:
                    # no tables found on this page
                    continue

                for tbl_idx, table in enumerate(page_tables):
                    if not table:
                        continue
                    # table is list of rows; convert to DataFrame
                    try:
                        # Heuristically treat first row as header if all elements are strings and not None
                        header = None
                        first_row = table[0]
                        if all(isinstance(c, str) for c in first_row):
                            header = first_row
                            data_rows = table[1:]
                        else:
                            data_rows = table

                        df = pd.DataFrame(data_rows, columns=header) if header is not None else pd.DataFrame(data_rows)

                        out_fname = f"{pdf_path.stem}_page{page_idx+1}_table{tbl_idx+1}.csv"
                        out_path = out_dir / out_fname
                        df.to_csv(out_path, index=False)
                        tables_written += 1
                        print(f"Wrote: {out_path}")
                    except Exception as e:
                        print(f"Error writing table {tbl_idx+1} from {pdf_path.name} page {page_idx+1}: {e}")
                        continue
    except Exception as e:
        print(f"Failed to open {pdf_path}: {e}")

    return tables_written


def main():
    parser = argparse.ArgumentParser(description="Extract tables from PDFs to CSVs")
    parser.add_argument("--pdf-dir", type=str, default="data_raw/raw_pdfs",
                        help="Directory containing PDF files (default: data_raw/raw_pdfs)")
    parser.add_argument("--out-dir", type=str, default="data_raw/csvs",
                        help="Directory to write CSV files (default: data_raw/csvs)")
    parser.add_argument("--recursive", action="store_true", help="Recursively search pdf-dir for PDFs")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of PDFs processed (0 = no limit)")

    args = parser.parse_args()

    pdf_dir = Path(args.pdf_dir)
    out_dir = Path(args.out_dir)

    if not pdf_dir.exists() or not pdf_dir.is_dir():
        print(f"PDF directory does not exist: {pdf_dir}")
        sys.exit(1)

    out_dir.mkdir(parents=True, exist_ok=True)

    pdfs = find_pdfs(pdf_dir, recursive=args.recursive)
    if not pdfs:
        print(f"No PDF files found in {pdf_dir}")
        return

    total_tables = 0
    processed = 0
    for pdf_path in pdfs:
        if args.limit and processed >= args.limit:
            break
        print(f"Processing: {pdf_path}")
        n = extract_tables_from_pdf(pdf_path, out_dir)
        total_tables += n
        processed += 1

    print(f"Done. Processed {processed} PDFs. Wrote {total_tables} tables to {out_dir}")


if __name__ == "__main__":
    main()

import argparse

from data_understand.jupyter_notebook_generator import \
    generate_jupyter_notebook
from data_understand.pdf_generator import generate_pdf


def parse_args():
    # Create Argument Parser
    parser = argparse.ArgumentParser(description="data.understand CLI")

    # Define Arguments
    parser.add_argument("-f", "--file_name", help="Directory path to CSV file")
    parser.add_argument(
        "-t", "--target_column", help="Target column name", default=None
    )
    parser.add_argument(
        "-p",
        "--generate_pdf",
        help="Generate PDF file for understanding of data",
        action="store_true",
    )
    parser.add_argument(
        "-j",
        "--generate_jupyter_notebook",
        help="Generate jupyter notebook file for understanding of data",
        action="store_true",
    )

    # Parse Arguments
    args = parser.parse_args()

    # Access Parsed Values
    print("file_name: " + args.file_name)
    print("target_column: " + args.target_column)
    print("generate_pdf: " + str(args.generate_pdf))
    print("generate_jupyter_notebook: " + str(args.generate_jupyter_notebook))

    return args


def main():
    args = parse_args()
    if args.generate_pdf:
        generate_pdf(args)

    if args.generate_jupyter_notebook:
        generate_jupyter_notebook(args)


if __name__ == "__main__":
    main()

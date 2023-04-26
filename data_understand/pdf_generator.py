from typing import Any

from fpdf import FPDF

from data_understand.load_dataset import load_dataset_as_dataframe


def generate_pdf(args: Any) -> None:
    dataframe = load_dataset_as_dataframe(args.file_name)
    print(dataframe.shape[0])
    print(dataframe.shape[1])

    pdf = FPDF()

    # Add the first page
    pdf.add_page()
    pdf.set_font("Arial", size=20)
    pdf.cell(200, 10, "Understanding the data in " + args.file_name, align="C")
    pdf.ln()
    pdf.set_font("Arial", size=11)
    pdf.cell(0, 10, "This PDF has different insights about your dataset.")
    pdf.ln()

    # Add an index to the document
    pdf.set_font("Arial", size=15)
    pdf.cell(0, 10, "Index")
    pdf.ln()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "Chapter 1 - Dataset Charateristics", link=pdf.add_link())

    # Add the dataset characteristics page
    pdf.add_page()
    pdf.set_font("Arial", size=20)
    pdf.cell(200, 10, "Chapter 1 - Dataset Charateristics", align="C")
    pdf.ln()
    pdf.set_font("Arial", size=11)
    pdf.cell(
        0,
        10,
        "The number of rows in the dataset are: " + str(dataframe.shape[0]),
    )
    pdf.ln()
    pdf.cell(
        0,
        10,
        "The number of columns in the dataset are: " + str(dataframe.shape[1]),
    )
    pdf.ln()
    pdf.cell(
        0,
        10,
        "The name of the target column is: " + args.target_column,
    )
    pdf.ln()

    pdf.output(args.file_name + ".pdf")

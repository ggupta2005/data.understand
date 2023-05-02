from typing import Any

from fpdf import FPDF

from data_understand.class_imbalance import get_message_target_column_imbalance
from data_understand.dataset_characteristics.characteristics import \
    get_message_columns_having_missing_values
from data_understand.feature_correlation import save_correlation_matrices
from data_understand.load_dataset import load_dataset_as_dataframe


class PDFReportGenerator(FPDF):
    def __init__(self, file_name, target_column_name):
        super(PDFReportGenerator, self).__init__()
        self._file_name = file_name
        self._target_column_name = target_column_name
        self._dataframe = load_dataset_as_dataframe(file_name)

    def add_title_and_description(self):
        # Add the first page
        self.add_page()
        self.set_font("Arial", size=20)
        self.cell(
            200, 10, "Understanding the data in " + self._file_name, align="C"
        )
        self.ln()
        self.ln()
        self.set_font("Arial", size=11)
        self.cell(0, 10, "This PDF has different insights about your dataset.")
        self.ln()

    def add_index(self):
        # Add an index to the document
        self.add_page()
        self.set_font("Arial", size=15)
        self.cell(0, 10, "Index")
        self.ln()
        self.set_font("Arial", size=12)
        self.cell(
            0, 10, "Chapter 1 - Dataset Charateristics", link=self.add_link()
        )

    def add_data_characteristics_page(self):
        # Add the dataset characteristics page
        self.add_page()
        self.set_font("Arial", size=20)
        self.cell(200, 10, "Chapter 1 - Dataset Charateristics", align="C")
        self.ln()
        self.set_font("Arial", size=11)
        self.cell(
            0,
            10,
            "The number of rows in the dataset are: "
            + str(self._dataframe.shape[0]),
        )
        self.ln()
        self.cell(
            0,
            10,
            "The number of columns in the dataset are: "
            + str(self._dataframe.shape[1]),
        )
        self.ln()
        self.cell(
            0,
            10,
            "The name of the target column is: " + self._target_column_name,
        )
        self.ln()
        self.cell(
            0,
            10,
            get_message_columns_having_missing_values(self._dataframe),
        )
        self.ln()

    def add_feature_correlation_page(self):
        save_correlation_matrices(self._dataframe)

        # Add a new page
        self.add_page()

        # Set the image dimensions
        width = 100
        height = 100

        # Load the image file
        image_file = "correlation.png"

        # Position the image on the page
        x = 10
        y = 10

        # Add the image to the page
        self.image(
            image_file,
            x,
            y,
            width,
            height,
            title="Correlation plots for numeric features",
        )

    def add_class_imbalance_page(self):
        # Add a new page
        self.add_page()
        self.set_font("Arial", size=20)
        self.cell(200, 10, "Chapter 3 - Class Imbalance", align="C")
        self.ln()
        self.set_font("Arial", size=11)
        self.multi_cell(
            0,
            10,
            get_message_target_column_imbalance(
                self._dataframe, self._target_column_name
            ),
        )
        self.ln()

    def save_pdf(self):
        self.output(self._file_name + ".pdf")


def generate_pdf(args: Any) -> None:
    dataframe = load_dataset_as_dataframe(args.file_name)
    print(dataframe.shape[0])
    print(dataframe.shape[1])

    pdf_report_generator = PDFReportGenerator(
        args.file_name, args.target_column
    )
    pdf_report_generator.add_title_and_description()
    pdf_report_generator.add_data_characteristics_page()
    pdf_report_generator.add_feature_correlation_page()
    pdf_report_generator.add_class_imbalance_page()
    pdf_report_generator.save_pdf()

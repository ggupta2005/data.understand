from typing import Any

from fpdf import FPDF, Align

from data_understand.class_imbalance import get_message_target_column_imbalance
from data_understand.dataset_characteristics.characteristics import (
    get_column_types_as_tuple, get_message_columns_having_missing_values)
from data_understand.feature_correlation import (
    get_feature_correlations_as_tuple, save_correlation_matrices)
from data_understand.load_dataset import load_dataset_as_dataframe


class PDFReportGenerator(FPDF):
    def __init__(self, file_name, target_column_name):
        super(PDFReportGenerator, self).__init__()
        self._file_name = file_name
        self._target_column_name = target_column_name
        self._dataframe = load_dataset_as_dataframe(file_name)

    def _add_heading(self, message: str):
        self.set_font("Arial", size=20)
        self.cell(200, 10, message, align="C")
        self.ln()

    def _add_sub_heading(self, message: str):
        self.set_font("Arial", size=15)
        self.cell(None, None, message)
        self.ln()

    def _add_text(self, message: str, multi_line=False):
        self.set_font("Arial", size=11)
        if multi_line:
            self.multi_cell(0, 10, message)
        else:
            self.cell(0, 10, message)
        self.ln()

    def add_title_and_description_page(self):
        # Add the first page
        self.add_page()
        self._add_heading(
            message="Understanding the data in " + self._file_name
        )
        self._add_text(
            message="This PDF has different insights about your dataset."
        )

    def add_index_page(self):
        # Add an index to the document
        self.add_page()
        self._add_sub_heading(message="Index")
        self._add_text("Chapter 1 - Dataset Charateristics")
        self._add_text("Chapter 2 - Visualize distributions of the dataset")
        self._add_text("Chapter 3 - Class Imbalance")

    def add_data_characteristics_page(self):
        # Add the dataset characteristics page
        self.add_page()
        self._add_heading("Chapter 1 - Dataset Charateristics")
        self._add_text(
            "The number of rows in the dataset are: "
            + str(self._dataframe.shape[0])
        )

        self._add_text(
            "The number of columns in the dataset are: "
            + str(self._dataframe.shape[1]),
        )

        self._add_text(
            "The name of the target column is: " + self._target_column_name,
        )

        self._add_text(
            get_message_columns_having_missing_values(self._dataframe),
        )

        self._add_text("The table of data type for each column is below:-")
        dataset_snapshot_table = get_column_types_as_tuple(self._dataframe)
        with self.table(text_align="CENTER") as table:
            for data_row in dataset_snapshot_table:
                row = table.row()
                for datum in data_row:
                    row.cell(datum)

    def add_feature_correlation_page(self):
        # Add a new page
        self.add_page()
        self._add_heading("Chapter 2 - Visualize distributions of the dataset")
        self._add_text(
            "This section have graphs and tables using which you can "
            "visualize distibutions of different features in your dataset, "
            "visualize the distibution of various categories for "
            "categorical features and find correlations between "
            "different features.",
            multi_line=True,
        )
        self._add_sub_heading("Feature Correlations")

        self._add_text("Top five positive feature correlations")
        positive_feature_correlation_table = get_feature_correlations_as_tuple(
            self._dataframe, 5, True
        )
        with self.table(text_align="CENTER") as table:
            for data_row in positive_feature_correlation_table:
                row = table.row()
                for datum in data_row:
                    row.cell(datum)
        self.ln()

        self._add_text("Top five negative feature correlations")
        negative_feature_correlation_table = get_feature_correlations_as_tuple(
            self._dataframe, 5, False
        )
        with self.table(text_align="CENTER") as table:
            for data_row in negative_feature_correlation_table:
                row = table.row()
                for datum in data_row:
                    row.cell(datum)
        self.ln()

        self.add_page()
        self._add_text("Feature correlation graph for numerical features")
        save_correlation_matrices(self._dataframe)
        # Add the image to the page
        self.image(
            "correlation.png",
            Align.C,
            y=10,
            w=100,
            h=100,
            title="Correlation plots for numeric features",
        )

    def add_class_imbalance_page(self):
        # Add a new page
        self.add_page()
        self._add_heading("Chapter 3 - Class Imbalance")
        self._add_text(
            get_message_target_column_imbalance(
                self._dataframe, self._target_column_name
            ),
            multi_line=True,
        )

    def save_pdf(self):
        self.output(self._file_name + ".pdf")


def generate_pdf(args: Any) -> None:
    dataframe = load_dataset_as_dataframe(args.file_name)
    print(dataframe.shape[0])
    print(dataframe.shape[1])

    pdf_report_generator = PDFReportGenerator(
        args.file_name, args.target_column
    )
    pdf_report_generator.add_title_and_description_page()
    pdf_report_generator.add_index_page()
    pdf_report_generator.add_data_characteristics_page()
    pdf_report_generator.add_feature_correlation_page()
    pdf_report_generator.add_class_imbalance_page()
    pdf_report_generator.save_pdf()

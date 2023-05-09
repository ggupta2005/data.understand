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

        self.cell(0, 10, "The table of data type for each column is below:-")
        self.ln()
        dataset_snapshot_table = get_column_types_as_tuple(self._dataframe)
        with self.table(text_align="CENTER") as table:
            for data_row in dataset_snapshot_table:
                row = table.row()
                for datum in data_row:
                    row.cell(datum)

    def add_feature_correlation_page(self):
        # Add a new page
        self.add_page()
        self.set_font("Arial", size=20)
        self.cell(
            200,
            10,
            "Chapter 2 - Visualize distributions of the dataset",
            align=Align.C,
        )
        self.ln()

        self.set_font("Arial", size=11)
        self.multi_cell(
            0,
            10,
            "This section have graphs and tables using which you can "
            "visualize distibutions of different features in your dataset, "
            "visualize the distibution of various categories for "
            "categorical features and find correlations between "
            "different features.",
        )
        self.ln()

        self.set_font("Arial", size=15)
        self.cell(None, None, "Feature Correlations")
        self.ln()

        self.set_font("Arial", size=11)
        self.cell(0, 10, "Top five positive feature correlations")
        self.ln()
        positive_feature_correlation_table = get_feature_correlations_as_tuple(
            self._dataframe, 5, True
        )
        with self.table(text_align="CENTER") as table:
            for data_row in positive_feature_correlation_table:
                row = table.row()
                for datum in data_row:
                    row.cell(datum)
        self.ln()

        self.set_font("Arial", size=11)
        self.cell(0, 10, "Top five negative feature correlations")
        self.ln()
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
        self.set_font("Arial", size=11)
        self.cell(200, 10, "Feature correlation graph for numerical features")
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

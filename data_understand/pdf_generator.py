import os
from typing import Any, Tuple

from fpdf import FPDF, Align

from data_understand.class_imbalance import get_message_target_column_imbalance
from data_understand.dataset_characteristics.characteristics import (
    get_column_types_as_tuple, get_message_columns_having_missing_values)
from data_understand.feature_correlation import (
    get_feature_correlations_as_tuple, save_correlation_matrices)
from data_understand.load_dataset import load_dataset_as_dataframe
from data_understand.messages import DATA_CHARATERISTICS_MESSAGE, MAIN_MESSAGE
from data_understand.utils import get_ml_task_type, measure_time
from data_understand.value_distributions import (
    save_box_plot_distributions, save_cat_frequency_distributions,
    save_histogram_distributions)


class PDFReportGenerator(FPDF):
    def __init__(self, file_name, target_column_name):
        super(PDFReportGenerator, self).__init__()
        self._file_name = file_name
        self._target_column_name = target_column_name
        self._dataframe = load_dataset_as_dataframe(file_name)

    def header(self):
        # Add watermark in the header
        self.set_font("Arial", "B", 50)
        self.set_text_color(128, 128, 128)
        self.rotate(45)
        self.text(-50, 150, "data.understand")
        self.rotate(0)
        self.set_text_color(0, 0, 0)
        self.set_font("Arial", "", 12)

    def footer(self):
        self.set_y(-15)  # Position the footer 15 units from the bottom
        self.set_font("Arial", size=11)  # Set font and style for the footer
        self.cell(
            0, 10, f"{self.page_no()}", 0, 0, "C"
        )  # Print the page number centered

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

    def _add_table(self, message: str, dataset_as_tuples: Tuple[Tuple[Any]]):
        self._add_text(message)
        with self.table(text_align="CENTER") as table:
            for data_row in dataset_as_tuples:
                row = table.row()
                for datum in data_row:
                    row.cell(datum)
        self.ln()

    def add_title_and_description_page(self):
        # Add the first page
        self.add_page()
        self._add_heading(
            message="Understanding the data in " + self._file_name
        )
        self._add_text(
            message=MAIN_MESSAGE.format("PDF report"), multi_line=True
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

        self._add_text(message=DATA_CHARATERISTICS_MESSAGE, multi_line=True)
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
            "The machine learning task based on your target column looks like: "
            + get_ml_task_type(self._dataframe, self._target_column_name)
        )

        self._add_text(
            get_message_columns_having_missing_values(self._dataframe),
        )

        dataset_snapshot_table = get_column_types_as_tuple(self._dataframe)
        self._add_table(
            "The table of data type for each column is below:-",
            dataset_snapshot_table,
        )

    def add_data_visualization_pages(self):
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
        self._add_cat_frequency_page()
        self._add_value_distribution_page()
        self._add_box_plot_page()
        self._add_feature_correlation_page()

    def _add_feature_correlation_page(self):
        self.add_page()
        self._add_sub_heading("Feature Correlations")

        positive_feature_correlation_table = get_feature_correlations_as_tuple(
            self._dataframe, 5, True
        )
        self._add_table(
            "Top five positive feature correlations",
            positive_feature_correlation_table,
        )

        negative_feature_correlation_table = get_feature_correlations_as_tuple(
            self._dataframe, 5, False
        )
        self._add_table(
            "Top five negative feature correlations",
            negative_feature_correlation_table,
        )

        self.add_page()
        self._add_text("Feature correlation graph for numerical features")
        save_correlation_matrices(self._dataframe)
        # Add the image to the page
        self.image(
            "correlation.png",
            Align.C,
            y=30,
            w=200,
            h=200,
            title="Correlation plots for numeric features",
        )
        os.remove("correlation.png")

    def _add_cat_frequency_page(self):
        self.add_page()
        self._add_sub_heading("Categorical feature distribution")
        save_cat_frequency_distributions(self._dataframe)

        index = 0
        page_index = 0
        while os.path.exists("cat_frequency_{0}.png".format(index)):
            if index > 0 and index % 4 == 0:
                self.add_page()
                page_index = 0

            if page_index % 2 == 0:
                self.image(
                    "cat_frequency_{0}.png".format(index),
                    Align.L,
                    y=40 + (page_index // 2) * 90,
                    w=90,
                    h=90,
                    title="Categorical value distribution",
                )
            else:
                self.image(
                    "cat_frequency_{0}.png".format(index),
                    Align.R,
                    y=40 + (page_index // 2) * 90,
                    w=90,
                    h=90,
                    title="Categorical value distribution",
                )
            os.remove("cat_frequency_{0}.png".format(index))

            page_index += 1
            index += 1

        if index == 0:
            self._add_text("No categorical features exists in the dataset.")

    def _add_value_distribution_page(self):
        self.add_page()
        self._add_sub_heading("Numerical value distribution")
        save_histogram_distributions(self._dataframe)

        index = 0
        page_index = 0
        while os.path.exists("value_distribution_{0}.png".format(index)):
            if index > 0 and index % 4 == 0:
                self.add_page()
                page_index = 0

            if page_index % 2 == 0:
                self.image(
                    "value_distribution_{0}.png".format(index),
                    Align.L,
                    y=40 + (page_index // 2) * 90,
                    w=90,
                    h=90,
                    title="Numerical value distribution",
                )
            else:
                self.image(
                    "value_distribution_{0}.png".format(index),
                    Align.R,
                    y=40 + (page_index // 2) * 90,
                    w=90,
                    h=90,
                    title="Numerical value distribution",
                )
            os.remove("value_distribution_{0}.png".format(index))

            page_index += 1
            index += 1

        if index == 0:
            self._add_text("No numerical features exists in the dataset.")

    def _add_box_plot_page(self):
        self.add_page()
        self._add_sub_heading("Box plot distribution")
        save_box_plot_distributions(self._dataframe)

        index = 0
        page_index = 0
        while os.path.exists("box_plot_{0}.png".format(index)):
            if index > 0 and index % 4 == 0:
                self.add_page()
                page_index = 0

            if page_index % 2 == 0:
                self.image(
                    "box_plot_{0}.png".format(index),
                    Align.L,
                    y=40 + (page_index // 2) * 90,
                    w=90,
                    h=90,
                    title="Categorical value distribution",
                )
            else:
                self.image(
                    "box_plot_{0}.png".format(index),
                    Align.R,
                    y=40 + (page_index // 2) * 90,
                    w=90,
                    h=90,
                    title="Categorical value distribution",
                )
            os.remove("box_plot_{0}.png".format(index))

            page_index += 1
            index += 1

        if index == 0:
            self._add_text("No categorical features exists in the dataset.")

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


@measure_time
def generate_pdf(args: Any) -> None:
    print("Generating PDF report for the dataset in " + args.file_name)
    pdf_report_generator = PDFReportGenerator(
        args.file_name, args.target_column
    )
    pdf_report_generator.add_title_and_description_page()
    pdf_report_generator.add_index_page()
    pdf_report_generator.add_data_characteristics_page()
    pdf_report_generator.add_data_visualization_pages()
    pdf_report_generator.add_class_imbalance_page()
    pdf_report_generator.save_pdf()
    print(
        "Successfully generated PDF report for the dataset in "
        + args.file_name
        + " at "
        + args.file_name
        + ".pdf"
    )

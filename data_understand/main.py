import argparse

import nbformat
from dataset_characteristics import (
    get_jupyter_nb_code_to_dataframe_head,
    get_jupyter_nb_code_to_dataframe_types,
    get_jupyter_nb_code_to_find_columns_having_missing_values)
from dataset_statistics import (get_jupyter_nb_code_to_dataframe_num_cols,
                                get_jupyter_nb_code_to_dataframe_num_rows)
from feature_correlation import \
    get_jupyter_nb_code_to_generate_correlation_matrices
from load_dataset import (get_jupyter_nb_code_to_read_as_dataframe,
                          load_dataset_as_dataframe)
from nbformat import v4
from value_distributions import (
    get_jupyter_nb_code_to_generate_cat_frequency_distributions,
    get_jupyter_nb_code_to_generate_histogram_distributions)


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


if __name__ == "__main__":
    args = parse_args()
    if args.generate_pdf:
        dataframe = load_dataset_as_dataframe(args.file_name)
        print(dataframe.shape[0])
        print(dataframe.shape[1])

    if args.generate_jupyter_notebook:
        nb = v4.new_notebook()
        (
            dataframe_read_markdown,
            dataframe_read_code,
        ) = get_jupyter_nb_code_to_read_as_dataframe(args.file_name)

        (
            dataframe_rows_markdown,
            dataframe_rows_code,
        ) = get_jupyter_nb_code_to_dataframe_num_rows()

        (
            dataframe_cols_markdown,
            dataframe_cols_code,
        ) = get_jupyter_nb_code_to_dataframe_num_cols()

        (
            dataframe_types_markdown,
            dataframe_types_code,
        ) = get_jupyter_nb_code_to_dataframe_types()

        (
            dataframe_head_markdown,
            dataframe_head_code,
        ) = get_jupyter_nb_code_to_dataframe_head()
        (
            historgram_markdown,
            histogram_code,
        ) = get_jupyter_nb_code_to_generate_histogram_distributions()
        (
            missing_values_markdown,
            missing_values_code,
        ) = get_jupyter_nb_code_to_find_columns_having_missing_values()
        (
            frequency_markdown,
            frequency_code,
        ) = get_jupyter_nb_code_to_generate_cat_frequency_distributions()
        (
            feature_correlation_markdown,
            feature_correlation_code,
        ) = get_jupyter_nb_code_to_generate_correlation_matrices()
        nb["cells"] = [
            v4.new_markdown_cell(source=dataframe_read_markdown),
            v4.new_code_cell(source=dataframe_read_code),
            v4.new_markdown_cell(source="## Display dataset statistics"),
            v4.new_markdown_cell(source=dataframe_rows_markdown),
            v4.new_code_cell(source=dataframe_rows_code),
            v4.new_markdown_cell(source=dataframe_cols_markdown),
            v4.new_code_cell(source=dataframe_cols_code),
            v4.new_markdown_cell(
                source="## Visualize characteristics of dataset"
            ),
            v4.new_markdown_cell(source=dataframe_types_markdown),
            v4.new_code_cell(source=dataframe_types_code),
            v4.new_markdown_cell(source=missing_values_markdown),
            v4.new_code_cell(source=missing_values_code),
            v4.new_markdown_cell(source=dataframe_head_markdown),
            v4.new_code_cell(source=dataframe_head_code),
            v4.new_markdown_cell(source=historgram_markdown),
            v4.new_code_cell(source=histogram_code),
            v4.new_markdown_cell(source=frequency_markdown),
            v4.new_code_cell(source=frequency_code),
            v4.new_markdown_cell(source=feature_correlation_markdown),
            v4.new_code_cell(source=feature_correlation_code),
        ]

        with open(args.file_name + ".ipynb", "w") as f:
            nbformat.write(nb, f)

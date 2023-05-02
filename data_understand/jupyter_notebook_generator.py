from typing import Any

import nbformat
from nbformat import v4

from data_understand.class_imbalance import \
    get_jupyter_nb_code_to_find_target_column_imbalance
from data_understand.dataset_characteristics import (
    get_jupyter_nb_code_to_dataframe_head,
    get_jupyter_nb_code_to_dataframe_types,
    get_jupyter_nb_code_to_find_columns_having_missing_values)
from data_understand.dataset_statistics import (
    get_jupyter_nb_code_to_dataframe_num_cols,
    get_jupyter_nb_code_to_dataframe_num_rows)
from data_understand.feature_correlation import \
    get_jupyter_nb_code_to_generate_correlation_matrices
from data_understand.load_dataset import \
    get_jupyter_nb_code_to_read_as_dataframe
from data_understand.target_characteristics import \
    get_jupyter_nb_code_to_get_target
from data_understand.value_distributions import (
    get_jupyter_nb_code_to_generate_cat_frequency_distributions,
    get_jupyter_nb_code_to_generate_histogram_distributions)


def generate_jupyter_notebook(args: Any) -> None:
    nb = v4.new_notebook()
    nb.metadata["title"] = "Understanding the data in " + args.file_name
    (
        dataframe_read_markdown,
        dataframe_read_code,
    ) = get_jupyter_nb_code_to_read_as_dataframe(args.file_name)
    (
        target_read_markdown,
        target_read_code,
    ) = get_jupyter_nb_code_to_get_target(args.target_column)
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
    (
        class_imbalance_markdown,
        class_imbalance_code,
    ) = get_jupyter_nb_code_to_find_target_column_imbalance()
    nb["cells"] = [
        v4.new_markdown_cell(source="## Read dataset and set target column"),
        v4.new_markdown_cell(source=dataframe_read_markdown),
        v4.new_code_cell(source=dataframe_read_code),
        v4.new_markdown_cell(source=target_read_markdown),
        v4.new_code_cell(source=target_read_code),
        v4.new_markdown_cell(source="## Display dataset statistics"),
        v4.new_markdown_cell(source=dataframe_rows_markdown),
        v4.new_code_cell(source=dataframe_rows_code),
        v4.new_markdown_cell(source=dataframe_cols_markdown),
        v4.new_code_cell(source=dataframe_cols_code),
        v4.new_markdown_cell(source="## Visualize characteristics of dataset"),
        v4.new_markdown_cell(source=dataframe_types_markdown),
        v4.new_code_cell(source=dataframe_types_code),
        v4.new_markdown_cell(source=missing_values_markdown),
        v4.new_code_cell(source=missing_values_code),
        v4.new_markdown_cell(source=dataframe_head_markdown),
        v4.new_code_cell(source=dataframe_head_code),
        v4.new_markdown_cell(
            source="## Visualize distributions of the dataset"
        ),
        v4.new_markdown_cell(source=historgram_markdown),
        v4.new_code_cell(source=histogram_code),
        v4.new_markdown_cell(source=frequency_markdown),
        v4.new_code_cell(source=frequency_code),
        v4.new_markdown_cell(source=feature_correlation_markdown),
        v4.new_code_cell(source=feature_correlation_code),
        v4.new_markdown_cell(
            source="## Find target column imbalances in "
                   "classification scenarios"
        ),
        v4.new_markdown_cell(source=class_imbalance_markdown),
        v4.new_code_cell(source=class_imbalance_code),
    ]

    with open(args.file_name + ".ipynb", "w") as f:
        nbformat.write(nb, f)

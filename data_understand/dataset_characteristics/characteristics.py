from typing import List, Tuple

import numpy as np
import pandas as pd


def find_columns_having_missing_values(df: pd.DataFrame) -> List[str]:
    columns_having_missing_values = []
    for feature in df.columns.tolist():
        if np.any(df[feature].isnull()):
            columns_having_missing_values.append(feature)
    return columns_having_missing_values


def get_jupyter_nb_code_to_dataframe_types() -> Tuple[str, str]:
    markdown = "### Display the types of dataset."
    code = "df.dtypes"
    return markdown, code


def get_jupyter_nb_code_to_dataframe_head() -> Tuple[str, str]:
    markdown = "### Display the first ten rows of dataset."
    code = "df.head(10)"
    return markdown, code


def get_jupyter_nb_code_to_find_columns_having_missing_values() -> (
    Tuple[str, str]
):
    markdown = "### Find if any features having missing values"
    code = (
        "from data_understand.dataset_characteristics import "
        + "find_columns_having_missing_values\n"
        + "find_columns_having_missing_values(df)"
    )
    return markdown, code

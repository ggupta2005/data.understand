from typing import Tuple

import numpy as np
import pandas as pd


def get_message_target_column_imbalance(
    df: pd.DataFrame, target_column: str
) -> str:
    target_column_array = df[target_column].values
    unique_array, element_counts = np.unique(
        target_column_array, return_counts=True
    )
    if len(unique_array) > 0.3 * len(target_column_array):
        return "The target column values look to be continous in nature. " + \
            "So cannot report class imbalance."
    max_class_count = max(element_counts)
    max_class = unique_array[
        np.argwhere(element_counts == max_class_count)[0][0]
    ]

    output_str = "The majority class is: {0}\n".format(max_class)
    for element, count in zip(unique_array, element_counts):
        if max_class != element:
            output_str += "The ratio of number of instance of majority " +\
                          "class {0} to class {1} is: {2}\n".format(
                            max_class, element, max_class_count / count)

    return output_str


def find_target_column_imbalance(df: pd.DataFrame, target_column: str) -> None:
    print(get_message_target_column_imbalance(df, target_column))


def get_jupyter_nb_code_to_find_target_column_imbalance() -> Tuple[str, str]:
    markdown = "### Find if there is any class imbalance in the " + \
        "dataset for classification scenarios."
    code = (
        "from data_understand.class_imbalance import "
        + "find_target_column_imbalance\n"
        + "find_target_column_imbalance(df, target_column)"
    )
    return markdown, code

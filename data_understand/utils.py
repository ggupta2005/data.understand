import timeit
from typing import Optional

import numpy as np
import pandas as pd

SEPARATOR_LENGTH = 120


def measure_time(compute_func):
    def compute_wrapper(*args, **kwargs):
        print(get_separator(SEPARATOR_LENGTH))
        start_time = timeit.default_timer()
        result = compute_func(*args, **kwargs)
        elapsed = timeit.default_timer() - start_time
        m, s = divmod(elapsed, 60)
        print("Time taken: {0} min {1} sec".format(m, s))
        print(get_separator(SEPARATOR_LENGTH))
        return result

    return compute_wrapper


def get_separator(max_len: int) -> str:
    return "=" * max_len


def get_ml_task_type(df: pd.DataFrame, target_column: str) -> str:
    target_column_array = df[target_column].values
    unique_array, element_counts = np.unique(
        target_column_array, return_counts=True
    )
    if len(unique_array) > 0.1 * len(target_column_array):
        return "Regression"
    return "Classification"


def construct_image_name(
    image_name: str,
    current_execution_uuid: str,
    index: Optional[int] = None,
    extension: Optional[str] = ".png",
):
    if index is not None:
        return (
            image_name
            + "_"
            + current_execution_uuid
            + "_"
            + str(index)
            + extension
        )
    else:
        return image_name + "_" + current_execution_uuid + extension

from typing import Tuple

import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import scatter_matrix


def _get_number_figures(df: pd.DataFrame) -> int:
    if df.shape[1] < 10:
        num_figures = 10
    else:
        num_figures = df.shape[1]
    return num_figures


def generate_correlation_matrices(df: pd.DataFrame) -> None:
    num_figures = _get_number_figures(df)
    scatter_matrix(df, figsize=(num_figures, num_figures))
    plt.show()


def save_correlation_matrices(df: pd.DataFrame) -> None:
    num_figures = _get_number_figures(df)
    scatter_matrix(df, figsize=(num_figures, num_figures))
    plt.savefig("correlation.png")


def get_jupyter_nb_code_to_generate_correlation_matrices() -> Tuple[str, str]:
    markdown = "### Generate feature correlation for numerical features"
    code = (
        "from data_understand.feature_correlation import "
        + "generate_correlation_matrices\n"
        + "generate_correlation_matrices(df)"
    )
    return markdown, code

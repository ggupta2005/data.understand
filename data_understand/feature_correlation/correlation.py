from typing import Tuple

import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import scatter_matrix


def generate_correlation_matrices(df: pd.DataFrame) -> None:
    if df.shape[1] < 10:
        num_figures = 10
    else:
        num_figures = df.shape[1]
    scatter_matrix(df, figsize=(num_figures, num_figures))
    plt.show()


def get_jupyter_nb_code_to_generate_correlation_matrices() -> Tuple[str, str]:
    markdown = "### Generate feature correlation for numerical features"
    code = (
        "from data_understand.feature_correlation import "
        + "generate_correlation_matrices\n"
        + "generate_correlation_matrices(df)"
    )
    return markdown, code

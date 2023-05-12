from typing import Any, Optional, Tuple

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
    plt.clf()


def get_jupyter_nb_code_to_generate_correlation_matrices() -> Tuple[str, str]:
    markdown = "### Generate feature correlation for numerical features"
    code = (
        "from data_understand.feature_correlation import "
        + "generate_correlation_matrices\n"
        + "generate_correlation_matrices(df)"
    )
    return markdown, code


def _get_top_k_correlated_feature_pairs(
    df: pd.DataFrame, positive_correlation: bool
) -> pd.DataFrame:
    corr_matrix = df.corr()

    corr_pairs = corr_matrix.unstack().reset_index()
    corr_pairs = corr_pairs[corr_pairs["level_0"] < corr_pairs["level_1"]]
    corr_pairs.columns = ["feature1", "feature2", "correlation"]

    if positive_correlation:
        return corr_pairs[corr_pairs["correlation"] > 0].sort_values(
            "correlation", ascending=False
        )

    return corr_pairs[corr_pairs["correlation"] < 0].sort_values(
        "correlation", ascending=True
    )


def get_top_k_postively_correlated_feature_pairs(
    df: pd.DataFrame, k: Optional[int] = 5
) -> pd.DataFrame:
    return _get_top_k_correlated_feature_pairs(df, True).head(k)


def get_top_k_negatively_correlated_feature_pairs(
    df: pd.DataFrame, k: Optional[int] = 5
) -> pd.DataFrame:
    return _get_top_k_correlated_feature_pairs(df, False).head(k)


def get_jupyter_nb_code_to_get_postively_correlated_feature_pairs() -> (
    Tuple[str, str]
):
    markdown = (
        "### Generate a table for numerical features pairs having "
        + "positive feature correlation"
    )
    code = (
        "from data_understand.feature_correlation import "
        + "get_top_k_postively_correlated_feature_pairs\n"
        + "get_top_k_postively_correlated_feature_pairs(df, 5)"
    )
    return markdown, code


def get_jupyter_nb_code_to_get_negatively_correlated_feature_pairs() -> (
    Tuple[str, str]
):
    markdown = (
        "### Generate a table for numerical features pairs having "
        + "negative feature correlation"
    )
    code = (
        "from data_understand.feature_correlation import "
        + "get_top_k_negatively_correlated_feature_pairs\n"
        + "get_top_k_negatively_correlated_feature_pairs(df, 5)"
    )
    return markdown, code


def get_feature_correlations_as_tuple(
    df: pd.DataFrame, k: int, positive_correlation: bool
) -> Tuple[Tuple[Any]]:
    if positive_correlation:
        correlation_df = get_top_k_postively_correlated_feature_pairs(df, k)
    else:
        correlation_df = get_top_k_negatively_correlated_feature_pairs(df, k)

    correlation_df["correlation"] = correlation_df["correlation"].astype(str)
    header_list = list(correlation_df.columns)

    return tuple(
        [tuple(header_list)] + list(correlation_df.to_records(index=False))
    )

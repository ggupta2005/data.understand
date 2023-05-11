from typing import Dict, Tuple

import matplotlib.pyplot as plt
import pandas as pd


def _generate_cat_frequency(df: pd.DataFrame) -> Dict[str, pd.Series]:
    numeric_features = set(df.select_dtypes(include="number").columns.tolist())
    all_features = set(df.columns.tolist())
    categorical_features = list(all_features - numeric_features)

    value_counts_dict = {}
    for feature in categorical_features:
        counts = df[feature].value_counts()
        value_counts_dict[feature] = counts

    return value_counts_dict


def generate_cat_frequency_distributions(df: pd.DataFrame) -> None:
    value_counts_dict = _generate_cat_frequency(df)
    for key in value_counts_dict:
        value_counts_dict[key].plot(kind="bar")
        plt.title("Frequency of Categories")
        plt.xlabel(key)
        plt.ylabel("Count")
        plt.show()


def save_cat_frequency_distributions(df: pd.DataFrame) -> None:
    value_counts_dict = _generate_cat_frequency(df)
    index = 0

    for key in value_counts_dict:
        value_counts_dict[key].plot(kind="bar")
        plt.title("Frequency of Categories")
        plt.xlabel(key)
        plt.ylabel("Count")
        plt.savefig("cat_frequency_{0}.png".format(index))
        index += 1


def get_jupyter_nb_code_to_generate_cat_frequency_distributions() -> (
    Tuple[str, str]
):
    markdown = "### Generate frequency distribution for categorical features"
    code = (
        "from data_understand.value_distributions import "
        + "generate_cat_frequency_distributions\n"
        + "generate_cat_frequency_distributions(df)"
    )
    return markdown, code

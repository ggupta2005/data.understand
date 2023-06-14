from typing import Any, List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from data_understand.utils import construct_image_name


def _get_histogram_distribution(data: np.ndarray) -> Tuple[Any, Any]:
    np.random.seed(0)

    # Create a histogram of the data
    plt.hist(
        data,
        bins=30,
        density=True,
        alpha=0.5,
        color="blue",
        edgecolor="black",
    )

    # Overlay a Gaussian PDF on top of the histogram
    mu = np.mean(data)
    sigma = np.std(data)
    x = np.linspace(mu - 3 * sigma, mu + 3 * sigma, 100)
    plot = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(
        -0.5 * ((x - mu) / sigma) ** 2
    )

    return x, plot


def generate_histogram_distributions(df: pd.DataFrame) -> None:
    numeric_features = df.select_dtypes(include="number").columns.tolist()
    for feature in numeric_features:
        x, plot = _get_histogram_distribution(df[feature].values)
        plt.plot(x, plot, color="red", linewidth=2, label="Gaussian PDF")

        # Add labels and a legend
        plt.xlabel(feature)
        plt.ylabel("Y axis label")
        plt.legend()

        # Set the title
        plt.title("Distribution Plot")

        # Show the plot
        plt.show()


def save_histogram_distributions(
    df: pd.DataFrame, current_execution_uuid: str
) -> List[str]:
    numeric_features = df.select_dtypes(include="number").columns.tolist()
    index = 0
    saved_image_name_list = []

    for feature in numeric_features:
        x, plot = _get_histogram_distribution(df[feature].values)
        plt.plot(x, plot, color="red", linewidth=2, label="Gaussian PDF")

        # Add labels and a legend
        plt.xlabel(feature)
        plt.ylabel("Y axis label")
        plt.legend()

        # Set the title
        plt.title("Distribution Plot")
        saved_image_name = construct_image_name(
            "value_distribution", current_execution_uuid, index
        )
        plt.savefig(saved_image_name)
        saved_image_name_list.append(saved_image_name)
        index += 1
        plt.clf()

    return saved_image_name_list


def get_jupyter_nb_code_to_generate_histogram_distributions() -> (
    Tuple[str, str]
):
    markdown = "### Generate histogram distribution for continous features"
    code = (
        "from data_understand.value_distributions import "
        + "generate_histogram_distributions\n"
        + "generate_histogram_distributions(df)"
    )
    return markdown, code

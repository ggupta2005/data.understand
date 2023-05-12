from typing import Any, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


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


def save_histogram_distributions(df: pd.DataFrame) -> None:
    numeric_features = df.select_dtypes(include="number").columns.tolist()
    index = 0
    for feature in numeric_features:
        x, plot = _get_histogram_distribution(df[feature].values)
        plt.plot(x, plot, color="red", linewidth=2, label="Gaussian PDF")

        # Add labels and a legend
        plt.xlabel(feature)
        plt.ylabel("Y axis label")
        plt.legend()

        # Set the title
        plt.title("Distribution Plot")

        plt.savefig("value_distribution_{0}.png".format(index))
        index += 1
        plt.clf()


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

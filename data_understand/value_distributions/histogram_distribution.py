from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np


def generate_histogram_distributions(df):
    numeric_features = df.select_dtypes(include="number").columns.tolist()
    for feature in numeric_features:
        # Generate random data for the distribution
        np.random.seed(0)
        data = df[feature].values

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
        pdf = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(
            -0.5 * ((x - mu) / sigma) ** 2
        )
        plt.plot(x, pdf, color="red", linewidth=2, label="Gaussian PDF")

        # Add labels and a legend
        plt.xlabel(feature)
        plt.ylabel("Y axis label")
        plt.legend()

        # Set the title
        plt.title("Distribution Plot")

        # Show the plot
        plt.show()


def get_jupyter_nb_code_to_generate_histogram_distributions() -> (
    Tuple[str, str]
):
    markdown = "### Generate histogram distribution for continous features"
    code = (
        "from data_understand.value_distribution import "
        + "generate_histogram_distributions\n"
        + "generate_histogram_distributions(df)"
    )
    return markdown, code

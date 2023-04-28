import sys
from io import StringIO

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris

from data_understand.class_imbalance import (
    find_target_column_imbalance, get_message_target_column_imbalance)


class TestClassImbalance:
    def test_get_message_target_column_imbalance_classification(self):
        # Load the iris dataset
        iris = load_iris()

        # Create a Pandas DataFrame from the iris data
        df = pd.DataFrame(data=iris.data, columns=iris.feature_names)

        # Add the target variable to the DataFrame
        df["target"] = iris.target

        output_str = get_message_target_column_imbalance(df, "target")
        assert "The majority class is: 0" in output_str
        assert (
            "The ratio of number of instance of majority class 0 to " +
            "class 1 is: 1.0"
            in output_str
        )
        assert (
            "The ratio of number of instance of majority class 0 to " +
            "class 2 is: 1.0"
            in output_str
        )

    def test_get_message_target_column_imbalance_regression(self):
        # Generate random data
        np.random.seed(42)
        x = np.random.rand(200)
        y = 2 * x + 0.5 + np.random.normal(scale=0.1, size=len(x))

        # Create dataframe
        df = pd.DataFrame({"x": x, "target": y})

        output_str = get_message_target_column_imbalance(df, "target")

        assert (
            "The target column values look to be continous in nature. "
            "So cannot report class imbalance."
            in output_str
        )

    def test_find_target_column_imbalance_classification(self):
        # Load the iris dataset
        iris = load_iris()

        # Create a Pandas DataFrame from the iris data
        df = pd.DataFrame(data=iris.data, columns=iris.feature_names)

        # Add the target variable to the DataFrame
        df["target"] = iris.target

        sys.stdout = StringIO()

        find_target_column_imbalance(df, "target")
        output_str = sys.stdout.getvalue()
        assert "The majority class is: 0" in output_str
        assert (
            "The ratio of number of instance of majority class 0 to " +
            "class 1 is: 1.0"
            in output_str
        )
        assert (
            "The ratio of number of instance of majority class 0 to " +
            "class 2 is: 1.0"
            in output_str
        )

    def test_find_target_column_imbalance_regression(self):
        # Generate random data
        np.random.seed(42)
        x = np.random.rand(200)
        y = 2 * x + 0.5 + np.random.normal(scale=0.1, size=len(x))

        # Create dataframe
        df = pd.DataFrame({"x": x, "target": y})
        sys.stdout = StringIO()

        find_target_column_imbalance(df, "target")
        output_str = sys.stdout.getvalue()
        assert (
            "The target column values look to be continous in nature. "
            "So cannot report class imbalance."
            in output_str
        )

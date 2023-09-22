import random

import pandas as pd

from data_understand.value_distributions import \
    get_jupyter_nb_code_to_generate_box_plot_distributions
from data_understand.value_distributions.box_plot_distribution import \
    _prune_categorical_feature_list


class TestHistogramDistribution:
    def test_get_jupyter_nb_code_to_generate_box_plot_distributions(self):
        (
            markdown,
            code,
        ) = get_jupyter_nb_code_to_generate_box_plot_distributions()
        assert isinstance(markdown, str)
        assert isinstance(code, str)

    def test_prune_categorical_feature_list(self):
        # Define the number of rows in the DataFrame
        num_rows = 100

        # Create a list of categories for each categorical column
        categories_less_than_15 = ["Category_A", "Category_B", "Category_C"]
        categories_exactly_15 = [f"Category_{i}" for i in range(1, 16)]
        categories_more_than_15 = ["Category_XYZ", "Category_ABC"] + [
            f"Category_{i}" for i in range(16, 31)
        ]

        # Create a dictionary to store data for each column
        data = {
            "Categorical_Column_1": random.choices(
                categories_less_than_15, k=num_rows
            ),
            "Categorical_Column_2": random.choices(
                categories_exactly_15, k=num_rows
            ),
            "Categorical_Column_3": random.choices(
                categories_more_than_15, k=num_rows
            ),
            "Numeric_Column": [
                random.randint(1, 100) for _ in range(num_rows)
            ],
        }

        # Create the DataFrame
        df = pd.DataFrame(data)

        pruned_categorical_feature_list = _prune_categorical_feature_list(
            df,
            [
                "Categorical_Column_1",
                "Categorical_Column_2",
                "Categorical_Column_3",
            ],
        )
        assert pruned_categorical_feature_list == [
            "Categorical_Column_1",
            "Categorical_Column_2",
        ]

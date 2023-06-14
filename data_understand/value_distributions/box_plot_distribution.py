from typing import List

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from data_understand.utils import construct_image_name
from data_understand.value_distributions.distribution_utils import \
    get_categorical_features


def save_box_plot_distributions(
    df: pd.DataFrame, current_execution_uuid: str
) -> List[str]:
    index = 0
    (
        numerical_feature_list,
        categorical_feature_list,
    ) = get_categorical_features(df)
    saved_image_name_list = []
    for numerical_feature in numerical_feature_list:
        for categorical_feature in categorical_feature_list:
            sns.boxplot(x=numerical_feature, y=categorical_feature, data=df)
            plt.xlabel(numerical_feature)
            plt.ylabel(categorical_feature)
            plt.title("Box Plot")

            saved_image_name = construct_image_name(
                "box_plot", current_execution_uuid, index
            )
            plt.savefig(saved_image_name)
            saved_image_name_list.append(saved_image_name)
            index += 1

            plt.clf()

    return saved_image_name_list

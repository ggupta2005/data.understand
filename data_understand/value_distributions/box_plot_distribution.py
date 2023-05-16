import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from data_understand.value_distributions.distribution_utils import \
    get_categorical_features


def save_box_plot_distributions(df: pd.DataFrame) -> None:
    index = 0
    (
        numerical_feature_list,
        categorical_feature_list,
    ) = get_categorical_features(df)
    for numerical_feature in numerical_feature_list:
        for categorical_feature in categorical_feature_list:
            sns.boxplot(x=numerical_feature, y=categorical_feature, data=df)
            plt.xlabel(numerical_feature)
            plt.ylabel(categorical_feature)
            plt.title("Box Plot")

            plt.savefig("box_plot_{0}.png".format(index))
            index += 1
            plt.clf()

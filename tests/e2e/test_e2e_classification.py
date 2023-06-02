import subprocess

import pandas as pd
import pytest
from rai_test_utils.datasets.tabular import (create_adult_census_data,
                                             create_cancer_data,
                                             create_iris_data,
                                             create_simple_titanic_data,
                                             create_wine_data)

from .common import TestE2ECommon


@pytest.mark.e2e_tests()
class TestE2EClassification(TestE2ECommon):
    @pytest.mark.parametrize(
        "dataset_name", ["iris", "titanic", "cancer", "wine", "adult"]
    )
    def test_e2e_classification(self, dataset_name):
        dataset_to_fixture_dict = {
            "iris": create_iris_data,
            "cancer": create_cancer_data,
            "wine": create_wine_data,
            "titanic": create_simple_titanic_data,
            "adult": create_adult_census_data,
        }
        dataset = dataset_to_fixture_dict[dataset_name]

        if dataset_name == "adult":
            X_train, _, y_train, _, _ = dataset()
        else:
            X_train, _, y_train, _, feature_names, _ = dataset()
        if not isinstance(X_train, pd.DataFrame):
            X_train = pd.DataFrame(data=X_train, columns=feature_names)

        X_train["target"] = y_train
        X_train.to_csv(dataset_name + ".csv", index=False)
        csv_file_name = dataset_name + ".csv"

        command = "data_understand -f {0} -t target -p -j".format(
            csv_file_name
        )
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True
        )
        assert result.returncode == 0

        self.verify_if_files_generated(csv_file_name)
        self.verify_jupyter_notebook(csv_file_name + ".ipynb")
        self.verify_pdf_file(csv_file_name + ".pdf")

        # Clean up the temporary files
        self.cleanup_generated_files(csv_file_name)

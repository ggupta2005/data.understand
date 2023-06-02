import subprocess

import pandas as pd
import pytest
from common import TestE2ECommon
from rai_test_utils.datasets.tabular import (create_diabetes_data,
                                             create_housing_data)


@pytest.mark.e2e_tests()
class TestE2ERegression(TestE2ECommon):
    @pytest.mark.parametrize("dataset_name", ["diabetes", "housing"])
    def test_e2e_regression(self, dataset_name):
        dataset_to_fixture_dict = {
            "diabetes": create_diabetes_data,
            "housing": create_housing_data,
        }
        dataset = dataset_to_fixture_dict[dataset_name]
        X_train, X_test, y_train, y_test, feature_names = dataset()
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

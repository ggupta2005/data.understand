from rai_test_utils.datasets.tabular import (
    create_adult_census_data, create_binary_classification_dataset,
    create_cancer_data, create_diabetes_data, create_housing_data,
    create_iris_data, create_simple_titanic_data, create_wine_data)
import pytest
import pandas as pd
import subprocess
import os

@pytest.mark.e2e_tests()
class TestE2ERegression:
    @pytest.mark.parametrize('dataset_name', ['diabetes', 'housing'])
    def test_e2e_regression(self, dataset_name):
        dataset_to_fixture_dict = {
           'diabetes': create_diabetes_data,
           'housing': create_housing_data
        }
        dataset = dataset_to_fixture_dict[dataset_name]
        X_train, X_test, y_train, y_test, feature_names = \
            dataset()
        if not isinstance(X_train, pd.DataFrame):
            X_train = pd.DataFrame(data=X_train, columns=feature_names)

        X_train['target'] = y_train
        X_train.to_csv(dataset_name + '.csv', index=False)
        csv_file_name = dataset_name + '.csv'

        command = 'data_understand -f {0} -t target -p -j'.format(csv_file_name)
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        assert result.returncode == 0
        assert os.path.exists(csv_file_name + '.pdf')
        assert os.path.exists(csv_file_name + '.ipynb')
        
        # Clean up the temporary files
        os.remove(csv_file_name)
        os.remove(csv_file_name + '.pdf')
        os.remove(csv_file_name + '.ipynb')
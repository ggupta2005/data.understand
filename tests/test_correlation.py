import pandas as pd

from data_understand.feature_correlation import \
    get_jupyter_nb_code_to_generate_correlation_matrices
from data_understand.feature_correlation.correlation import _get_number_figures


class TestFeatureCorrelation:
    def test_get_number_figures(self):
        few_features_data = {
            "Name": ["John", "Anna", "Peter", "Linda"],
            "Age": [25, 30, 21, 40],
            "Gender": ["Male", "Female", "Male", "Female"],
            "Salary": [50000, 75000, 40000, 90000],
        }

        few_features_df = pd.DataFrame(few_features_data)

        assert 10 == _get_number_figures(few_features_df)

        more_features_data = {
            "Name": ["John", "Anna", "Peter", "Linda"],
            "Age": [25, 30, 21, 40],
            "Gender": ["Male", "Female", "Male", "Female"],
            "Salary": [50000, 75000, 40000, 90000],
            "Department": ["Sales", "Marketing", "Engineering", "Finance"],
            "Hire Date": [
                "2020-05-01",
                "2019-08-01",
                "2021-01-15",
                "2018-12-01",
            ],
            "Title": [
                "Sales Representative",
                "Marketing Manager",
                "Software Engineer",
                "Chief Financial Officer",
            ],
            "Location": ["New York", "Los Angeles", "Seattle", "Chicago"],
            "Experience": [2, 5, 1, 10],
            "Education": ["Bachelor", "Master", "Bachelor", "PhD"],
            "Language": ["English", "Spanish", "Java", "Python"],
            "Nationality": ["American", "German", "Chinese", "Canadian"],
        }

        more_features_df = pd.DataFrame(more_features_data)

        assert len(more_features_df.columns) == _get_number_figures(
            more_features_df
        )

    def test_get_jupyter_nb_code_to_generate_correlation_matrices(self):
        (
            markdown,
            code,
        ) = get_jupyter_nb_code_to_generate_correlation_matrices()
        assert isinstance(markdown, str)
        assert isinstance(code, str)

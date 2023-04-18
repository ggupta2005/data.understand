import pandas as pd

from data_understand.dataset_characteristics import (
    find_columns_having_missing_values, get_jupyter_nb_code_to_dataframe_head,
    get_jupyter_nb_code_to_dataframe_types)


class TestDatasetCharacteristics:
    def test_get_jupyter_nb_code_to_dataframe_types(self):
        markdown, code = get_jupyter_nb_code_to_dataframe_types()
        assert isinstance(markdown, str)
        assert isinstance(code, str)

    def test_get_jupyter_nb_code_to_dataframe_head(self):
        markdown, code = get_jupyter_nb_code_to_dataframe_head()
        assert isinstance(markdown, str)
        assert isinstance(code, str)

    def test_find_columns_having_missing_values(self):
        df_missing_values = pd.DataFrame(
            {"A": [1, None, 3], "B": [4, 5, None], "C": [4, 5, 9]}
        )
        columns_having_missing_values = find_columns_having_missing_values(
            df_missing_values
        )
        assert columns_having_missing_values == ["A", "B"]

        df_no_missing_values = pd.DataFrame(
            {"A": [1, 2, 3], "B": [4, 5, 5], "C": [4, 5, 9]}
        )
        columns_having_missing_values = find_columns_having_missing_values(
            df_no_missing_values
        )
        assert columns_having_missing_values == []

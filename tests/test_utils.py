import pandas as pd

from data_understand.utils import get_ml_task_type, get_separator, measure_time


class TestUtils:
    def test_get_separator(self):
        separation_str = get_separator(10)
        assert len(separation_str) == 10
        assert "=" * 10 == separation_str

    def test_measure_time(self):
        def mock_func(x):
            return x

        value = measure_time(mock_func)(10)
        assert value == 10

    def test_get_ml_task_type(self):
        classification_data = {
            "Column1": [
                1,
                2,
                3,
                4,
                5,
                1,
                2,
                3,
                4,
                5,
                1,
                2,
                3,
                4,
                5,
                1,
                2,
                3,
                4,
                5,
            ],
            "Column2": [
                "A",
                "A",
                "C",
                "C",
                "A",
                "A",
                "A",
                "C",
                "C",
                "A",
                "A",
                "A",
                "C",
                "C",
                "A",
                "A",
                "A",
                "C",
                "C",
                "A",
            ],
        }
        classification_df = pd.DataFrame(classification_data)
        assert (
            get_ml_task_type(classification_df, "Column2") == "Classification"
        )

        regression_data = {
            "Column1": [1, 2, 3, 4, 5],
            "Column2": ["A", "B", "C", "C", "E"],
        }
        regression_df = pd.DataFrame(regression_data)
        assert get_ml_task_type(regression_df, "Column2") == "Regression"

from data_understand.utils import get_separator, measure_time


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

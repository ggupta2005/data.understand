from data_understand.feature_correlation import \
    get_jupyter_nb_code_to_generate_correlation_matrices


class TestFeatureCorrelation:
    def test_get_jupyter_nb_code_to_generate_correlation_matrices(self):
        (
            markdown,
            code,
        ) = get_jupyter_nb_code_to_generate_correlation_matrices()
        assert isinstance(markdown, str)
        assert isinstance(code, str)

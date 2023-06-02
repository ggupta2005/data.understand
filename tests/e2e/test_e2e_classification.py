import os
import subprocess
import tempfile

import nbformat
import pandas as pd
import pytest
from rai_test_utils.datasets.tabular import (create_adult_census_data,
                                             create_cancer_data,
                                             create_iris_data,
                                             create_simple_titanic_data,
                                             create_wine_data)


@pytest.mark.e2e_tests()
class TestE2EClassification:
    def verify_jupyter_notebook(self, jupyter_notebook_file_name):
        self._verify_jupyter_notebook_output_cells_are_empty(
            jupyter_notebook_file_name
        )
        self._run_and_verify_jupyter_notebook_output_cells(
            jupyter_notebook_file_name
        )

    def _verify_jupyter_notebook_output_cells_are_empty(
        self, jupyter_notebook_file_name
    ):
        with open(jupyter_notebook_file_name, "r") as file:
            # Parse the notebook file using nbformat
            notebook = nbformat.read(file, as_version=4)

        for cell in notebook.cells:
            if "outputs" in cell:
                assert (
                    len(cell["outputs"]) == 0
                ), "Output cell found in notebook. Please clean your notebook"

    def _run_and_verify_jupyter_notebook_output_cells(self, filepath):
        """Execute a notebook via nbconvert and collect output."""
        with tempfile.NamedTemporaryFile(suffix=".ipynb") as fout:
            args = [
                "jupyter",
                "nbconvert",
                "--to",
                "notebook",
                "--execute",
                "-y",
                "--no-prompt",
                "--output",
                fout.name,
                filepath,
            ]
            subprocess.check_call(args)

            fout.seek(0)
            nb = nbformat.read(fout, nbformat.current_nbformat)

        errors = [
            output
            for cell in nb.cells
            if "outputs" in cell
            for output in cell["outputs"]
            if output.output_type == "error"
        ]

        assert (
            errors == []
        ), "There shouldn't be any errors in the executed jupyter notebook"

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
        assert os.path.exists(csv_file_name + ".pdf")
        assert os.path.exists(csv_file_name + ".ipynb")

        self.verify_jupyter_notebook(csv_file_name + ".ipynb")

        # Clean up the temporary files
        os.remove(csv_file_name)
        os.remove(csv_file_name + ".pdf")
        os.remove(csv_file_name + ".ipynb")

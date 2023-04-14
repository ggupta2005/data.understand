from typing import Tuple


def get_jupyter_nb_code_to_dataframe_num_rows() -> Tuple[str, str]:
    markdown = "### Get the number of rows in pandas dataframe"
    code = "df.shape[0]"
    return markdown, code


def get_jupyter_nb_code_to_dataframe_num_cols() -> Tuple[str, str]:
    markdown = "### Get the number of columns in pandas dataframe"
    code = "df.shape[1]"
    return markdown, code

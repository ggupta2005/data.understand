from typing import Tuple


def get_jupyter_nb_code_to_dataframe_types() -> Tuple[str, str]:
    markdown = "### Display the types of dataset."
    code = "df.dtypes"
    return markdown, code


def get_jupyter_nb_code_to_dataframe_head() -> Tuple[str, str]:
    markdown = "### Display the first ten rows of dataset."
    code = "df.head(10)"
    return markdown, code

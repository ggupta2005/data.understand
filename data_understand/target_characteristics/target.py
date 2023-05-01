from typing import Tuple


def get_jupyter_nb_code_to_get_target(target_column: str) -> Tuple[str, str]:
    markdown = "### Set the target column name"
    code = "target_column = '{}'".format(target_column)
    return markdown, code

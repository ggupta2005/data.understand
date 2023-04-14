import pandas as pd
from typing import Tuple


def load_dataset_as_dataframe(file_name: str) -> pd.DataFrame:
    return pd.read_csv(file_name)


def get_jupyter_nb_code_to_read_as_dataframe(
    file_name: str,
) -> Tuple[str, str]:
    markdown = "## Read the csv file as pandas dataframe"
    code = "import pandas as pd\ndf = pd.read_csv('{0}')".format(file_name)
    return markdown, code

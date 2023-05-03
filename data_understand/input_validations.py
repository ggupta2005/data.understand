import os
from typing import Any

import pandas as pd


def validate_input_parameters(args: Any) -> None:
    if args.file_name is None:
        raise Exception(
            "A valid file name {0} is required. "
            "Please provide a valid file path.".format(args.file_name)
        )

    if args.target_column is None:
        raise Exception("A valid target column name is required.")

    if not args.file_name.endswith(".csv"):
        raise Exception(
            "The file {} is not a CSV file. "
            "Please provide a CSV file.".format(args.file_name)
        )

    if not os.path.exists(args.file_name):
        raise Exception("The file {} doesn't exists.".format(args.file_name))

    try:
        df = pd.read_csv(args.file_name)
    except Exception:
        raise Exception(
            "Unable to read CSV file {0} as a pandas DataFrame".format(
                args.file_name
            )
        )

    if args.target_column not in df.columns.tolist():
        raise Exception(
            "The target column name {0} doesn't exist in dataset.".format(
                args.target_column
            )
        )

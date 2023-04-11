import argparse


def parse_args():
    # Create Argument Parser
    parser = argparse.ArgumentParser(description="data.understand CLI")

    # Define Arguments
    parser.add_argument("-f", "--file_name", help="Directory path to CSV file")
    parser.add_argument("-t", "--target_column", help="Target column name", default=None)

    # Parse Arguments
    args = parser.parse_args()

    # Access Parsed Values
    print("file_name", args.file_name)
    print("target_column", args.target_column)


if __name__ == "__main__":
    args = parse_args()

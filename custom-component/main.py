import argparse
import pandas as pd
from sklearn.model_selection import train_test_split

from pathlib import Path


def split_csv_file(input_file_path, ratio, train_output_path, test_output_path):
    try:
        df = pd.read_csv(input_file_path)
        
        df_train, df_test = train_test_split(df, test_size=ratio, random_state=42)
        
        Path(f"{train_output_path}/data").mkdir(parents=True, exist_ok=True)
        df_train.to_csv(f"{train_output_path}/data/train.csv", index=False)
        
        Path(f"{test_output_path}/data").mkdir(parents=True, exist_ok=True)
        df_test.to_csv(f"{test_output_path}/data/test.csv", index=False)
        
        print(f"CSV file split into {train_output_path} and {test_output_path} with ratio {ratio}")

    except FileNotFoundError:
        print(f"File not found: {input_file_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split CSV file into train and test data")
    parser.add_argument("--input_file_path", type=str, help="Path to input CSV file")
    parser.add_argument("--ratio", type=float, help="Ratio to split the data into two parts")
    parser.add_argument("--train_output_path", type=str, help="Path to save the training dataset")
    parser.add_argument("--test_output_path", type=str, help="Path to save the test dataset")
    args = parser.parse_args()

    split_csv_file(
        args.input_file_path, args.ratio, args.train_output_path, args.test_output_path
    )

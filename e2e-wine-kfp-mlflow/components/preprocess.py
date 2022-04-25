from kfp.components import InputPath, OutputPath


def preprocess(file_path: InputPath('CSV'),
               output_file: OutputPath('parquet')):
    import pandas as pd
    df = pd.read_csv(file_path, header=0, sep=";")
    df.columns = [c.lower().replace(' ', '_') for c in df.columns]
    df.to_parquet(output_file)

from kfp.components import InputPath


def train(file_path: InputPath('parquet')) -> str:
    import pandas as pd
    from sklearn.model_selection import train_test_split
    import mlflow
    from sklearn.linear_model import ElasticNet

    df = pd.read_parquet(file_path)

    target_column = 'quality'
    train_x, test_x, train_y, test_y = train_test_split(
        df.drop(columns=[target_column]),
        df[target_column], test_size=.25,
        random_state=1337, stratify=df[target_column])

    with mlflow.start_run(run_name='elastic_net_models'):
        alpha = 0.5
        l1_ratio = 0.5
        lr = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42)
        lr.fit(train_x, train_y)
        result = mlflow.sklearn.log_model(lr, "model",
                                          registered_model_name="wine-elasticnet")
        return f"{mlflow.get_artifact_uri()}/{result.artifact_path}"

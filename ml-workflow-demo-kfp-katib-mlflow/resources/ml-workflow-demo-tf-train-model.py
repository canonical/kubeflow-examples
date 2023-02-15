import tensorflow as tf
import pandas as pd
import logging
import mlflow
import mlflow.keras
import argparse
import os
import boto3
from io import StringIO

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%SZ",
)

# Instructions to get these VARs: https://github.com/canonical/mlflow-operator#get-minio-key-and-secret
# This assumes you have deployed MLFlow https://github.com/canonical/mlflow-operator#get-started
os.environ['MLFLOW_TRACKING_URI'] = "http://mlflow-server.kubeflow.svc.cluster.local:5000"
os.environ["MLFLOW_S3_ENDPOINT_URL"] = "http://minio.kubeflow.svc.cluster.local:9000"
os.environ["AWS_ACCESS_KEY_ID"] = os.getenv('accesskey', "")
os.environ["AWS_SECRET_ACCESS_KEY"] = os.getenv('secretkey', "")


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--tf-data-dir",
        type=str,
        default="/opt/data.csv",
        help="GCS path or local path of training data.",
    )
    parser.add_argument(
        "--tf-export-dir",
        type=str,
        default="mnist/",
        help="GCS path or local directory to export model",
    )
    parser.add_argument(
        "--tf-model-type",
        type=str,
        default="CNN",
        help="Tensorflow model type for training.",
    )
    parser.add_argument("--epochs", type=int, default=100, help="Number of epochs")

    parser.add_argument(
        "--s3-storage",
        type=bool,
        default=False,
        help="Enable fetching artifacts from s3",
    )
    parser.add_argument(
        "--bucket", type=str, default="dataset", help="Name of s3 bucket"
    )
    parser.add_argument(
        "--bucket-key", type=str, default="df.csv", help="Key of the object in s3"
    )
    parser.add_argument(
        "--mlflow-model-name", type=str, default="", help="Path to export the models"
    )
    parser.add_argument("--test", type=bool, default=False, help="Train with test data")

    args = parser.parse_known_args()[0]
    return args


args = parse_arguments()


def get_s3_object():
    s3 = boto3.client(
        "s3",
        endpoint_url="http://minio.kubeflow.svc.cluster.local:9000",
        aws_access_key_id=os.getenv('accesskey'),
        aws_secret_access_key=os.getenv('secretkey'),
    )
    response = s3.get_object(Bucket=args.bucket, Key=args.bucket_key)
    logging.info("S3 object loaded")
    return response


def model_function():
    model = tf.keras.Sequential(
        [
            tf.keras.layers.Dense(10, activation="relu"),
            tf.keras.layers.Dense(10, activation="relu"),
            tf.keras.layers.Dense(1, activation="softmax"),
        ]
    )
    return model


def get_csv_from_s3(response):
    r_bytes = r_bytes = response["Body"].read()
    s = str(r_bytes, "utf-8")
    data = StringIO(s)
    df = pd.read_csv(data)
    logging.info("Datafreame processed from S3 object")
    return df


def main():
    model = model_function()
    model.compile(
        optimizer="rmsprop", loss="categorical_crossentropy", metrics=["accuracy"]
    )
    logging.info(args.mlflow_model_name)

    if args.s3_storage:
        logging.info(f"Trying to use S3 dataset from {args.bucket}/{args.bucket_key}")
        response = get_s3_object()
        kdd_cup_data_clean = get_csv_from_s3(response)
    else:
        kdd_cup_data_clean = pd.read_csv(args.tf_data_dir)

    with mlflow.start_run(run_name="kdd_models"):
        X_train = kdd_cup_data_clean.loc[:, kdd_cup_data_clean.columns != "CHURN"]
        y_train = kdd_cup_data_clean["CHURN"]
        model.fit(X_train, y_train, batch_size=50, epochs=args.epochs)
        if args.mlflow_model_name != "":
            logging.info("Saving model to mlflow")
            result = mlflow.keras.log_model(model, "models", registered_model_name=args.mlflow_model_name)
            logging.info(f"Model saved to {mlflow.get_artifact_uri()}/{result.artifact_path}")
            return f"{mlflow.get_artifact_uri()}/{result.artifact_path}"

        X_test = kdd_cup_data_clean.loc[:, kdd_cup_data_clean.columns != "CHURN"]
        y_test = kdd_cup_data_clean["CHURN"]

        loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
        loss, accuracy = model.evaluate(X_test, y_test, verbose=0)

        logging.info(f"loss = {loss}")
        logging.info(f"accuracy = {accuracy}")


if __name__ == "__main__":
    main()

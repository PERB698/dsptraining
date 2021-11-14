import os
import pandas as pd
import numpy as np
import boto3
from joblib import dump
from joblib import load
import logging
from datetime import datetime

from constants.files import create_folder, S3_BUCKET

PROJECT_ROOT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",)
LOG_PATH = create_folder(os.path.join(PROJECT_ROOT_PATH, "logs"))

log_filename = datetime.now().strftime("%Y-%m-%d") + ".log"
LOG_FILE = os.path.join(LOG_PATH, log_filename)


def mean_absolute_percentage_error(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true))


def normalize_s3_filename(filename):
    # for Unix machines
    output_filename = filename.replace("/", "-")
    # for Windows machines
    output_filename = output_filename.replace("\\", "-")
    return output_filename


def upload_pandas_df_to_s3(df, s3_bucket, filename):
    s3_resource = boto3.resource('s3')

    df.to_csv(normalize_s3_filename(filename), index=False)
    s3_resource.Object(s3_bucket, filename).upload_file(Filename=normalize_s3_filename(filename))
    os.remove(normalize_s3_filename(filename))


def load_pandas_df_from_s3(s3_bucket, filename):
    s3_resource = boto3.resource('s3')

    s3_resource.Object(s3_bucket, filename).download_file(Filename=normalize_s3_filename(filename))
    df = pd.read_csv(normalize_s3_filename(filename))
    os.remove(normalize_s3_filename(filename))

    return df


def upload_ml_object_to_s3(pipeline_or_model, s3_bucket, filename):
    s3_resource = boto3.resource('s3')

    dump(pipeline_or_model, normalize_s3_filename(filename))
    s3_resource.Object(s3_bucket, filename).upload_file(Filename=normalize_s3_filename(filename))
    os.remove(normalize_s3_filename(filename))


def load_ml_object_from_s3(s3_bucket, filename):
    s3_resource = boto3.resource('s3')

    s3_resource.Object(s3_bucket, filename).download_file(Filename=normalize_s3_filename(filename))
    ml_object = load(normalize_s3_filename(filename))
    os.remove(normalize_s3_filename(filename))

    return ml_object


def setup_logs():
    logging_format = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format=logging_format)

    # Set up logging to console
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(logging.Formatter(logging_format))
    logging.getLogger('').addHandler(console)


def upload_logs_to_s3():
    s3_resource = boto3.resource('s3')

    s3_resource.Object(S3_BUCKET, f"data/logs/{log_filename}").upload_file(Filename=LOG_FILE)
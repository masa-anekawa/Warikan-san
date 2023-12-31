import os
import boto3
import pandas as pd
import logging

from io import BytesIO

# ロギングの設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)

INPUT_ENCODING = 'cp932'
OUTPUT_ENCODING = 'utf-8'

s3 = boto3.client('s3')


def lambda_handler(event, context):
    # Set the bucket and object key from the Lambda event (assuming the Lambda is triggered by S3)
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    input_file_key = event['Records'][0]['s3']['object']['key']

    input_df = load_df_from_s3(s3, bucket_name, input_file_key, encoding=INPUT_ENCODING)

    # set output bucket from env
    output_bucket_name = os.environ.get('OUTPUT_BUCKET', 'warikan-san-encoding-adjuster-outputs')
    # set output file key by adding '_formatted' to the input file key
    output_file_key = _format_output_file_key(input_file_key)

    save_df_to_s3(s3, input_df, output_bucket_name, output_file_key, encoding=OUTPUT_ENCODING)

    response = {
        'statusCode': 200,
        'body': f'Successfully transformed {input_file_key} and saved as {output_file_key}'
    }
    return response


def load_df_from_s3(s3, bucket_name, file_key, encoding='utf-8'):
    logger.info(f'loading file from {file_key}')
    response = s3.get_object(Bucket=bucket_name, Key=file_key)

    # response['Body'] may be either bytes or string. so transform it to bytes and decode it
    body = response['Body'].read()
    if isinstance(body, bytes):
        body_bytes = BytesIO(body)
    else: # isinstance(body, str):
        body_bytes = BytesIO(body.encode(encoding))

    df = pd.read_csv(body_bytes, encoding=encoding)
    return df


def save_df_to_s3(s3, df, bucket_name, output_file_key, encoding='utf-8'):
    logger.info(f'exporting file to {output_file_key}')
    csv_buffer = BytesIO()
    df.to_csv(csv_buffer, index=False, encoding=encoding)
    s3.put_object(Bucket=bucket_name, Key=output_file_key, Body=csv_buffer.getvalue())


def lambda_handler_local(event, context):
    input_file_key = './input_format.csv'
    output_file_key = './output/output_format.csv'
    # input_df = load_df_from_s3(s3, bucket_name, input_file_key)
    input_df = _load_df_from_file(input_file_key)
    output_df = transform_df(input_df)
    _save_df_to_file(output_df, output_file_key)

    response = {
        'statusCode': 200,
        'body': f'Successfully transformed {input_file_key} and saved as {output_file_key}'
    }
    logger.info(response)
    return response


def _load_df_from_file(file_path):
    df = pd.read_csv(file_path, encoding='utf-8')
    return df


def _save_df_to_file(df, output_file_path):
    df.to_csv(output_file_path, index=False, encoding='utf-8')


def _format_output_file_key(file_path):
    # Split the filepath into directory, base (filename without extension) and extension
    dir_name, file_name = os.path.split(file_path)
    base_name, ext = os.path.splitext(file_name)

    # Append '_formatted' to the base name
    formatted_name = base_name + '_adjusted' + ext

    # Combine the directory and the new file name to get the full path
    formatted_path = os.path.join(dir_name, formatted_name)

    return formatted_path

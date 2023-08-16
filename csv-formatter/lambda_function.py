import boto3
import pandas as pd
from io import StringIO

def lambda_handler(event, context):
    # Initialize S3 client
    s3 = boto3.client('s3')

    # Set the bucket and object key from the Lambda event (assuming the Lambda is triggered by S3)
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    input_file_key = event['Records'][0]['s3']['object']['key']

    input_df = load_df_from_s3(s3, bucket_name, input_file_key)
    output_df = transform_df(input_df)
    output_file_key = input_file_key.replace('.csv', '_transformed.csv')
    save_df_to_s3(s3, output_df, bucket_name, output_file_key)

    return {
        'statusCode': 200,
        'body': f'Successfully transformed {input_file_key} and saved as {output_file_key}'
    }


def load_df_from_s3(s3, bucket_name, file_key):
    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    input_file_content = response['Body'].read().decode('utf-8')
    df = pd.read_csv(StringIO(input_file_content))
    return df


def transform_df(input_df):
    output_df = pd.DataFrame()
    filtered_df = input_df[input_df['割り勘対象'] == 1]
    output_df['金額'] = -filtered_df['金額（円）']
    output_df['日付'] = filtered_df['日付']  # Rule 2
    output_df['支払い者'] = 'まさ'  # Rule 3
    output_df['品目'] = filtered_df['内容']  # Rule 4
    return output_df


def save_df_to_s3(s3, df, bucket_name, output_file_key):
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    s3.put_object(Bucket=bucket_name, Key=output_file_key, Body=csv_buffer.getvalue())

import boto3
import pandas as pd
from io import StringIO

def lambda_handler(event, context):
    # Initialize S3 client
    s3 = boto3.client('s3')

    # Set the bucket and object key from the Lambda event (assuming the Lambda is triggered by S3)
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    input_file_key = event['Records'][0]['s3']['object']['key']

    # Download the file from S3
    response = s3.get_object(Bucket=bucket_name, Key=input_file_key)
    input_file_content = response['Body'].read().decode('utf-8')
    input_df = pd.read_csv(StringIO(input_file_content))

    # Transform the file based on the defined rules
    output_df = pd.DataFrame()
    output_df['金額'] = -input_df['金額（円）']
    filtered_df = input_df[input_df['割り勘対象'] == 1]
    output_df['日付'] = filtered_df['日付']  # Rule 2
    output_df['支払い者'] = 'まさ'  # Rule 3
    output_df['品目'] = filtered_df['内容']  # Rule 4

    # Convert the transformed dataframe to CSV
    csv_buffer = StringIO()
    output_df.to_csv(csv_buffer, index=False)

    # Define the output key (e.g., appending '_transformed' to the input file name)
    output_file_key = input_file_key.replace('.csv', '_transformed.csv')

    # Upload the transformed file to S3
    s3.put_object(Bucket=bucket_name, Key=output_file_key, Body=csv_buffer.getvalue())

    return {
        'statusCode': 200,
        'body': f'Successfully transformed {input_file_key} and saved as {output_file_key}'
    }

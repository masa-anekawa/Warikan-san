import json
import boto3
import os
from io import StringIO

from src.main_inference import process_stream_for_inference

# simple as lambda handler that invoke specific function, called by s3 put event
def lambda_handler(event, context):
    print(event)
    print(context)
    # get s3 object
    s3 = boto3.client('s3')
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    # get object
    response = s3.get_object(Bucket=bucket, Key=key)
    # get body
    input_stream = response['Body']
    # create output stream from string io
    output_stream = StringIO()
    # process
    process_stream_for_inference(input_stream, output_stream)
    # upload to s3 where bucket and key is retrieved from env values
    output_bucket = os.environ.get('OUTPUT_BUCKET', 'warikan-detector-output')
    s3.put_object(Bucket=output_bucket, Key=key, Body=output_stream)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


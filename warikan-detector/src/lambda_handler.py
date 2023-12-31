import json
import boto3
import logging
import os
from io import BytesIO, TextIOWrapper

from src.main_inference import process_stream_for_inference

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


s3 = boto3.client('s3')


# simple as lambda handler that invoke specific function, called by s3 put event
def lambda_handler(event, context):
    logger.info(f'event: {event}')
    logger.info(f'context: {context}')

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    response = s3.get_object(Bucket=bucket, Key=key)
    input_stream = TextIOWrapper(response['Body'])
    output_buffer = BytesIO()
    output_stream = TextIOWrapper(output_buffer)

    process_stream_for_inference(input_stream, output_stream, model_save_path='models/xgboost_model.pkl')

    output_bucket = os.environ.get('OUTPUT_BUCKET', 'warikan-detector-output')
    s3.put_object(Bucket=output_bucket, Key=key, Body=output_buffer.getvalue())
    response = {
        'statusCode': 200,
        'body': f'Successfully processed {key} in {bucket} and saved as {key} in {output_bucket}'
    }
    logger.info(f'response: {response}')
    return response

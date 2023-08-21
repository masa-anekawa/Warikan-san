import boto3
import os
import logging

s3 = boto3.client('s3')

# ロギングの設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    # イベントからアップロードされたS3のオブジェクト情報を取得
    record = event['Records'][0]
    input_bucket = record['s3']['bucket']['name']
    input_key = record['s3']['object']['key']

    logger.info(f'Received file {input_key} from bucket {input_bucket}')

    # S3からファイルを取得
    file_obj = s3.get_object(Bucket=input_bucket, Key=input_key)
    file_content = file_obj['Body'].read()

    # ログにファイルの先頭部分を出力 (デバッグのため)
    logger.info(f'File content (first 100 bytes): {file_content[:100]}')

    # 変形せずにそのまま別のS3バケットに保存
    output_bucket = os.environ['OUTPUT_BUCKET']
    s3.put_object(Bucket=output_bucket, Key=f'output/{input_key}', Body=file_content)

    logger.info(f'File saved to {output_bucket}/output/{input_key}')

    return {
        'statusCode': 200,
        'body': f'Processed input file {input_key} from {input_bucket}'
    }

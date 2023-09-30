import os
import boto3
import gspread
import pandas as pd
import logging

from io import BytesIO

# ロギングの設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)

ENCODING = 'cp932'

s3 = boto3.client('s3')

# カラム名とデフォルト値のマッピング
COLUMN_DEFAULT_VALUE = {
    'マサミク': 'FALSE',
    '清算': 'FALSE',
    'まさ比率': 2,
    'まな比率': 1,
    '清算済み': 'FALSE',
    '重複？': 'FALSE'
}

def lambda_handler(event, context):
    # S3からオブジェクトを取得
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    df = load_df_from_s3(s3, bucket, key, encoding=ENCODING)
    append_df_to_gspread(df)

    response = {
        'statusCode': 200,
        'body': f'Successfully transformed {key} and saved as {key}'
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


def append_df_to_gspread(df: pd.DataFrame) -> None:
    # Google Spreadsheetに接続
    gc = gspread.service_account()
    sheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1j-7OXWMZ_GYTZ6UR1LUo5ro4px5ArHSRw7YYiZ4RHMY/edit#gid=458319299").worksheet("マスタ")
    existing_data = sheet.get_all_records()
    existing_df = pd.DataFrame(existing_data)
    # IDカラムをインクリメント
    assert(not existing_df.empty, 'Existing data is empty')
    last_id = existing_df['ID'].max()
    df['ID'] = range(last_id + 1, last_id + 1 + len(df))

    # カラム名のマッチングとデフォルト値の追記
    for col in existing_df.columns:
        if col not in df.columns:
            df[col] = 'Default_Value'  # ここで指定するデフォルト値

    # 新しいデータをGoogle Spreadsheetに追記
    for _, row in df.iterrows():
        sheet.append_row(row.tolist())

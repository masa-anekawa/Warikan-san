import os
import boto3
import gspread
import pandas as pd
import pprint
import logging

from io import BytesIO

from src.secrets_helper import get_secret_dict

# ロギングの設定
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')

# カラム名とデフォルト値のマッピング
COLUMN_DEFAULT_VALUE = {
    'マサミク': False,
    '清算': False,
    'まさ比率': 2,
    'まな比率': 1,
    '清算済み': False,
    '重複？': False
}


def lambda_handler(event, context):
    # S3からオブジェクトを取得
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    input_df = load_df_from_s3(s3, bucket, key)
    append_df_to_gspread(input_df)

    response = {
        'statusCode': 200,
        'body': f'Successfully transformed {key} and saved as {key}'
    }
    return response


def load_df_from_s3(s3, bucket_name, file_key):
    logger.info(f'loading file from {file_key}')
    response = s3.get_object(Bucket=bucket_name, Key=file_key)

    # response['Body'] may be either bytes or string. so transform it to bytes and decode it
    body = response['Body'].read()
    if isinstance(body, bytes):
        body_bytes = BytesIO(body)
    else: # isinstance(body, str):
        body_bytes = BytesIO(body.encode())

    df = pd.read_csv(body_bytes)
    return df


def append_df_to_gspread(input_df: pd.DataFrame) -> None:
    logger.info('appending dataframe to gspread...')

    # Google Spreadsheetに接続
    gc = _get_service_account()
    sheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1j-7OXWMZ_GYTZ6UR1LUo5ro4px5ArHSRw7YYiZ4RHMY/edit#gid=458319299").worksheet("マスタ")
    logger.info(f'connected to {sheet}')
    existing_data = sheet.get_all_records()
    existing_df = pd.DataFrame(existing_data)
    logger.info(f'existing_df: {existing_df.info}')

    output_df = _calc_output_df(input_df, existing_df)

    # find the range to be updated
    logger.info('finding the range to be updated...')
    first_update_row = existing_df.index[-1] + 2
    first_col = existing_df.columns.get_loc('ID')
    last_update_row = first_update_row + len(output_df) - 1
    last_col = existing_df.columns.get_loc('重複？')

    update_range_str = f'{_convert_index_to_alphabet(first_col)}{first_update_row}:{_convert_index_to_alphabet(last_col)}{last_update_row}'

    # call batch_update
    logger.info(f'updating range {update_range_str}...')
    sheet.batch_update([
        {
            'range': update_range_str,
            'values': output_df.to_dict('split')['data']
        }
    ])


def _get_service_account():
    """
    Returns a gspread service account object either from the secret manager or from the default credentials.
    """
    try:
        logger.info('trying to get service account from secret manager...')
        credentials = get_secret_dict(os.environ['SECRETS_NAME'])
        service_account = gspread.service_account_from_dict(credentials)
    # Catch any exception and try to get service account from default credentials
    except Exception as e:
        logger.warn(f'Failed to get service account from secret manager: {e}. Trying to get from default credentials...')
        service_account = gspread.service_account()
    return service_account

def _calc_output_df(input_df: pd.DataFrame, existing_df: pd.DataFrame) -> pd.DataFrame:
    logger.info('transforming dataframe to output...')

    output_df = input_df.copy()
    pprint.pprint(output_df)

    # IDカラムをインクリメント
    last_id = existing_df['ID'].max()
    output_df['ID'] = range(last_id + 1, last_id + 1 + len(input_df))
    pprint.pprint(output_df)

    # カラム名のマッチングとデフォルト値の追記
    for col, default_value in COLUMN_DEFAULT_VALUE.items():
        if col not in output_df.columns:
            output_df[col] = default_value
    pprint.pprint(output_df)

    # 「まさ負担額」、「まな負担額」は行ごとの計算が必要
    output_df['まさ負担額'] = output_df['金額'] * output_df['まさ比率'] // (output_df['まさ比率'] + output_df['まな比率'])
    output_df['まな負担額'] = output_df['金額'] - output_df['まさ負担額']

    # Rearrange columns so that it matches the order of existing_df
    output_df = output_df[existing_df.columns]

    return output_df


def _convert_index_to_alphabet(index: int) -> str:
    """Converts 0-based index to alphabet, e.g. 0 -> A, 1 -> B, 26 -> AA, 27 -> AB"""
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if index < len(alphabet):
        return alphabet[index]
    else:
        return _convert_index_to_alphabet(index // len(alphabet) - 1) + alphabet[index % len(alphabet)]
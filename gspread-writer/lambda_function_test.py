import pandas as pd
from io import BytesIO
from unittest.mock import MagicMock, patch, ANY, call
import unittest

import lambda_function


class TestLambdaFunction(unittest.TestCase):
    EVENT = {
        'Records': [
            {
                's3': {
                    'bucket': {
                        'name': 'test-bucket'
                    },
                    'object': {
                        'key': 'test-key'
                    }
                }
            }
        ]
    }
    ENCODING = 'cp932'
    INPUT_BYTES = 'input content\n'.encode(ENCODING)
    OUTPUT_BYTES = 'output content\n'.encode(ENCODING)
    GSPREAD_RECORDS = pd.read_csv('./gspread_format.csv').to_dict()

    def setUp(self):
        self.mock_s3 = patch.object(lambda_function, 's3').start()
        self.mock_gspread_service_account = patch.object(lambda_function.gspread, 'service_account').start()
        self.mock_sheet = self._mock_gspread_records()

    def tearDown(self):
        patch.stopall()

    def test_lambda_handler_writes_to_gspread_with_correct_arguments(self):
        # Set up mock S3 response
        self._mock_s3_body(self.INPUT_BYTES)
        mock_sheet = self._mock_gspread_records()

        # Call lambda_handler function
        lambda_function.lambda_handler(self.EVENT, None)

        # Assert that S3 client was called with correct arguments
        self.mock_s3.get_object.assert_called_once_with(Bucket='test-bucket', Key='test-key')
        mock_sheet.batch_update.assert_called_once_with([
            {
                'range': 'A2:M2',
                'values': [[656,1490,'2023/8/26','まさ','ガジェット','FALSE','FALSE',2,1,8643,4322,'FALSE','FALSE']]
            },
            {
                'range': 'A3:M3',
                'values': [[657,489,'2023/8/25','まさ','ドラッグストア','FALSE','FALSE',2,1,8643,4322,'FALSE','FALSE']]
            }
        ])

    def test_lambda_handler_handles_input_and_output_with_s3(self):
        # Set up mock S3 response
        body_content = BytesIO(self.INPUT_BYTES)
        mock_response = {
            'Body': body_content
        }
        self.mock_s3.get_object.return_value = mock_response

        # mock transform_df
        def mock_transform_df(input_df):
            return pd.read_csv(BytesIO(self.OUTPUT_BYTES))
        lambda_function.transform_df = mock_transform_df

        # Call lambda_handler function
        lambda_function.lambda_handler(self.EVENT, None)

        # Assert that S3 client was called with correct arguments
        self.mock_s3.get_object.assert_called_once_with(Bucket='test-bucket', Key='test-key')
        self.mock_s3.put_object.assert_not_called()

    def _mock_s3_body(self, body_bytes: bytes):
        body_content = BytesIO(body_bytes)
        mock_response = {
            'Body': body_content
        }
        self.mock_s3.get_object.return_value = mock_response

    def _mock_gspread_records(self):
        self.mock_gspread_service_account.open_by_url.return_value = MagicMock()
        mock_sheet = MagicMock()
        self.mock_gspread_service_account.open_by_url.return_value.worksheet.return_value = mock_sheet
        mock_sheet.get_all_records.return_value = self.GSPREAD_RECORDS
        return mock_sheet

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
    EXISTING_GSPREAD_RECORDS = pd.read_csv('./gspread_format.csv').to_dict()
    INPUT_DF = pd.read_csv('./input_format.csv')

    mock_s3 = None
    mock_gspread = None

    @classmethod
    def setUpClass(cls):
        cls.mock_s3 = patch.object(lambda_function, 's3').start()
        cls.mock_gspread = patch.object(lambda_function, 'gspread').start()

    @classmethod
    def tearDownClass(cls):
        patch.stopall()

    def setUp(self):
        self.mock_sheet = self._mock_gspread_records()

    def tearDown(self):
        self.mock_sheet.reset_mock()

    def test_lambda_handler_writes_to_gspread_with_correct_arguments(self):
        # Set up mock S3 response
        self._mock_input()

        # Call lambda_handler function
        lambda_function.lambda_handler(self.EVENT, None)

        # Assert that S3 client was called with correct arguments
        self.mock_s3.get_object.assert_called_once_with(Bucket='test-bucket', Key='test-key')
        self.mock_sheet.batch_update.assert_called_once_with([
            {
                'range': 'A2:M3',
                'values': [
                    [656,1490,'2023/8/26','まさ','ガジェット','FALSE','FALSE',2,1,993,497,'FALSE','FALSE'],
                    [657,489,'2023/8/25','まさ','ドラッグストア','FALSE','FALSE',2,1,326,163,'FALSE','FALSE']
                ]
            }
        ])

    def _mock_s3_body(self, body_bytes: bytes):
        body_content = BytesIO(body_bytes)
        mock_response = {
            'Body': body_content
        }
        self.mock_s3.get_object.return_value = mock_response

    def _mock_input(self):
        # Prepare bytes that is read from input_format.csv, and call _mock_s3_body with it
        input_bytes = BytesIO()
        self.INPUT_DF.to_csv(input_bytes, index=False, encoding=self.ENCODING)
        self._mock_s3_body(input_bytes.getvalue())

    def _mock_gspread_records(self):
        mock_sheet = MagicMock()
        self.mock_gspread.service_account.return_value.open_by_url.return_value.worksheet.return_value = mock_sheet
        mock_sheet.get_all_records.return_value = self.EXISTING_GSPREAD_RECORDS
        return mock_sheet

import json
import unittest
from unittest.mock import MagicMock, patch, ANY

from src import lambda_handler

class TestLambdaHandler(unittest.TestCase):
    @patch.object(lambda_handler, 'process_stream_for_inference')
    @patch.object(lambda_handler, 'boto3')
    def test_lambda_handler(self, mock_boto3, mock_process_stream_for_inference):
        # Mock S3 client
        mock_client = MagicMock()
        mock_boto3.client.return_value = mock_client

        # Mock S3 response
        mock_response = {'Body': MagicMock()}
        mock_client.get_object.return_value = mock_response

        # Call lambda_handler
        event = {
            'Records': [
                {
                    's3': {
                        'bucket': {'name': 'test-bucket'},
                        'object': {'key': 'test-key'}
                    }
                }
            ]
        }
        context = MagicMock()
        response = lambda_handler.lambda_handler(event, context)

        # Assert S3 client was called with correct arguments
        mock_boto3.client.assert_called_once_with('s3')
        mock_client.get_object.assert_called_once_with(
            Bucket='test-bucket',
            Key='test-key'
        )

        # Assert S3 client was called with correct arguments to upload output.
        mock_client.put_object.assert_called_once_with(
            Bucket='warikan-detector-output',
            Key='test-key',
            Body=ANY
        )

        # Assert process_stream_for_inference was called with correct arguments
        mock_process_stream_for_inference.assert_called_once_with(
            mock_response['Body'],
            ANY
        )

        # Assert lambda_handler returns correct response
        expected_response = {
            'statusCode': 200,
            'body': json.dumps('Hello from Lambda!')
        }
        self.assertEqual(response, expected_response)

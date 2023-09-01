import json
import boto3
from io import StringIO, BytesIO, TextIOWrapper
import unittest
from unittest.mock import MagicMock, patch, ANY, call

from src import lambda_handler

@patch('src.lambda_handler.BytesIO')
@patch('src.lambda_handler.TextIOWrapper')
@patch.object(lambda_handler, 'process_stream_for_inference')
@patch.object(lambda_handler, 's3')
def test_lambda_handler(mock_s3, mock_process_stream_for_inference, mock_text_io_wrapper, mock_bytes_io):
    # Set up mock S3 event
    event = {
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

    # Set up mock S3 response
    body_content = BytesIO(b'abcdef')
    mock_response = {
        'Body': body_content
    }
    mock_s3.get_object.return_value = mock_response

    # Ser up mock input and output stream
    input_stream = TextIOWrapper(body_content, encoding='cp932')
    output_buffer = BytesIO()
    mock_bytes_io.return_value = output_buffer
    output_stream = TextIOWrapper(output_buffer, encoding='cp932')
    mock_text_io_wrapper.side_effect = [input_stream, output_stream]

    # Call lambda_handler function
    lambda_handler.lambda_handler(event, None)

    # Assert that S3 client was called with correct arguments
    mock_s3.get_object.assert_called_once_with(Bucket='test-bucket', Key='test-key')
    mock_s3.put_object.assert_called_once_with(Bucket='warikan-detector-output', Key='test-key', Body=output_buffer.getvalue())

    # Assert that the mock bytes io wrapper was called with correct arguments
    mock_bytes_io.assert_called_once_with()

    # Assert that the mock text io wrapper was called with correct arguments
    mock_text_io_wrapper.assert_has_calls([
        call(body_content, encoding='cp932'),
        call(output_buffer, encoding='cp932')
    ])

    # Assert that process_stream_for_inference was called with correct arguments
    mock_process_stream_for_inference.assert_called_once_with(input_stream, output_stream, model_save_path='models/xgboost_model.pkl')

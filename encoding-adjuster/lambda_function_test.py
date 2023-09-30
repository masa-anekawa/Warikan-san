import pandas as pd
from io import BytesIO
from unittest.mock import patch, ANY, call

import lambda_function


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
INPUT_ENCODING = 'cp932'
OUTPUT_ENCODING = 'utf-8'
INPUT_BYTES = 'content\n'.encode(INPUT_ENCODING)
OUTPUT_BYTES = 'content\n'.encode(OUTPUT_ENCODING)


@patch.object(lambda_function, 's3')
def test_lambda_handler_handles_input_and_output_with_s3(mock_s3):
    # Set up mock S3 response
    body_content = BytesIO(INPUT_BYTES)
    mock_response = {
        'Body': body_content
    }
    mock_s3.get_object.return_value = mock_response

    # Call lambda_handler function
    lambda_function.lambda_handler(EVENT, None)

    # Assert that S3 client was called with correct arguments
    mock_s3.get_object.assert_called_once_with(Bucket='test-bucket', Key='test-key')
    mock_s3.put_object.assert_called_once_with(Bucket='warikan-san-encoding-adjuster-outputs', Key='test-key_adjusted', Body=OUTPUT_BYTES)

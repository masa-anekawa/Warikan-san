import os
import shutil
import tempfile
import unittest
from unittest.mock import mock_open, patch
import pandas as pd

from src import main_inference

class TestProcessFolderForInference(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for input and output files
        self.input_dir = tempfile.mkdtemp()
        self.output_dir = tempfile.mkdtemp()

        # Create a test CSV file
        self.test_data = pd.DataFrame({
            '計算対象': [1, 1, 1],
            '日付': ['2022-01-01', '2022-01-02', '2022-01-03'],
            '内容': ['test', 'test', 'test'],
            '金額（円）': [-1000, -2000, -3000],
            '保有金融機関': ['test', 'test', 'test'],
            '大項目': ['test', 'test', 'test'],
            '中項目': ['test', 'test', 'test'],
            'メモ': ['test', 'test', ''],
            '振替': [0, 0, 0],
            'ID': ['1', '2', '3'],
        })
        self.test_file_path = os.path.join(self.input_dir, 'test.csv')
        self.test_file_path_2 = os.path.join(self.input_dir, 'test_2.csv')
        self.test_data.to_csv(self.test_file_path, index=False)
        self.test_data.to_csv(self.test_file_path_2, index=False)
        self.test_output_file_path = os.path.join(self.output_dir, 'predicted_test.csv')
        self.test_output_file_path_2 = os.path.join(self.output_dir, 'predicted_test_2.csv')

    def tearDown(self):
        # Remove the temporary directory and its contents
        shutil.rmtree(self.input_dir)
        shutil.rmtree(self.output_dir)

    @patch.object(main_inference, 'process_csv_file_for_inference')
    def test_process_folder_for_inference(self, mock_process_csv_file_for_inference):
        # Call the function with the test input and output directories
        main_inference.process_folder_for_inference(self.input_dir, self.output_dir)
        # Check that mocked function was called with the correct arguments
        mock_process_csv_file_for_inference.mock_calls[0].assert_called_once_with(self.test_file_path, self.test_output_file_path)
        mock_process_csv_file_for_inference.mock_calls[1].assert_called_once_with(self.test_file_path_2, self.test_output_file_path_2)

    @patch.object(main_inference, 'process_stream_for_inference')
    @patch('builtins.open', new_callable=mock_open)
    def test_process_csv_file_for_inference(self, mocked_open, mock_process_stream_for_inference):
        # Prepare input and output stream as magic mocks returned by mocked_open
        mock_input_stream = mocked_open.return_value
        mock_output_stream = mocked_open.return_value
        # Call the function with the test input and output files
        main_inference.process_csv_file_for_inference(self.test_file_path, self.test_output_file_path)
        # Check that the mocked function was called with the correct arguments
        mocked_open.mock_calls[0].assert_called_once_with(self.test_file_path)
        mocked_open.mock_calls[1].assert_called_once_with(self.test_output_file_path, 'w')
        mock_process_stream_for_inference.assert_called_with(mock_input_stream, mock_output_stream)

    def test_process_stream_for_inference(self):
        # Prepare the input and output streams
        input_stream = open(self.test_file_path)
        output_stream = open(self.test_output_file_path, 'a+')
        # Call the function with the test input and output directories
        main_inference.process_stream_for_inference(input_stream, output_stream, model_save_path='models/xgboost_model.pkl', encoder_save_path='models/label_encoders.pkl')
        # Check that the output file was created and has the correct content
        output_stream.seek(0)
        output_data = pd.read_csv(output_stream)
        self.assertEqual(output_data.shape, (3, 11))
        self.assertListEqual(list(output_data.columns), ['計算対象','日付','内容','金額（円）','保有金融機関','大項目','中項目','メモ','振替','ID','予測_割り勘対象'])
        self.assertListEqual(list(output_data['予測_割り勘対象']), [0, 0, 0])


if __name__ == '__main__':
    unittest.main()
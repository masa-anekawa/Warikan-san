import os
import shutil
import tempfile
import unittest
import pandas as pd
from src.main_inference import process_folder_for_inference, process_csv_for_inference

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
        self.test_data.to_csv(self.test_file_path, index=False, encoding='SHIFT_JIS')

    def tearDown(self):
        # Remove the temporary directory and its contents
        shutil.rmtree(self.input_dir)
        shutil.rmtree(self.output_dir)

    def test_process_folder_for_inference(self):
        # Call the function with the test input and output directories
        process_folder_for_inference(self.input_dir, self.output_dir)

        # Check that the output file was created and has the correct content
        output_file_path = os.path.join(self.output_dir, 'predicted_test.csv')
        self.assertTrue(os.path.exists(output_file_path))
        output_data = pd.read_csv(output_file_path, encoding='SHIFT_JIS')
        self.assertEqual(output_data.shape, (3, 11))
        self.assertListEqual(list(output_data.columns), ['計算対象','日付','内容','金額（円）','保有金融機関','大項目','中項目','メモ','振替','ID','予測_割り勘対象'])
        self.assertListEqual(list(output_data['予測_割り勘対象']), [0, 0, 0])


    def test_process_csv_for_inference(self):
        # Call the function with the test input and output directories
        output_data = process_csv_for_inference(self.test_file_path)

        # Check that the output file was created and has the correct content
        self.assertEqual(output_data.shape, (3, 11))
        self.assertListEqual(list(output_data.columns), ['計算対象','日付','内容','金額（円）','保有金融機関','大項目','中項目','メモ','振替','ID','予測_割り勘対象'])
        self.assertListEqual(list(output_data['予測_割り勘対象']), [0, 0, 0])

if __name__ == '__main__':
    unittest.main()
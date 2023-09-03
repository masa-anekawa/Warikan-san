import os
import pandas as pd
from joblib import load
import logging
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier

from src.preprocessing import preprocess_data_handle_unseen
from src.training import WarikanClassifier
from src.warikan_stream import WarikanStream

logger = logging.getLogger(__name__)


def process_folder_for_inference(input_folder_path, output_folder_path, **kwargs) -> None:
    # List all CSV files in the folder
    csv_files = [f for f in os.listdir(input_folder_path) if f.endswith('.csv')]
    # Process each CSV file
    for csv_file in csv_files:
        input_file_path = os.path.join(input_folder_path, csv_file)
        output_file_path = os.path.join(output_folder_path, "predicted_" + csv_file)
        process_csv_file_for_inference(input_file_path, output_file_path, **kwargs)


def process_csv_file_for_inference(input_file_path, output_file_path, **kwargs) -> None:
    # extract 'encoding' from kwargs
    encoding = kwargs.get('encoding', 'cp932')
    with open(input_file_path, 'r', encoding=encoding) as input, open(output_file_path, 'w', encoding=encoding) as output:
        process_stream_for_inference(input, output, **kwargs)


def process_stream_for_inference(input_stream: WarikanStream, output_stream: WarikanStream, **kwargs) -> None:
    # Load model and label encoders, overriding the default paths if necessary
    model_save_path = kwargs.get('model_save_path', 'models/random_forest_model.pkl')
    encoder_save_path = kwargs.get('encoder_save_path', 'models/label_encoders.pkl')
    logger.info(f'model_save_path: {model_save_path}')
    logger.info(f'encoder_save_path: {encoder_save_path}')
    clf: WarikanClassifier = load(model_save_path)
    label_encoder: LabelEncoder = load(encoder_save_path)
    # Load data
    data = pd.read_csv(input_stream)
    logger.info(f'Dataframe size: {data.shape}')
    # Preprocess data
    preprocessed_data = preprocess_data_handle_unseen(data, label_encoder)
    logger.info(f'Preprocessed dataframe size: {preprocessed_data.shape}')
    # Predict
    predictions = clf.predict(preprocessed_data)
    logger.info(f'{np.count_nonzero(predictions)} out of {len(predictions)} rows are predicted to be warikan')
    # Add predictions to original data
    data['予測_割り勘対象'] = predictions
    # Return the predicted data
    data.to_csv(output_stream, index=False)
    logger.info(f'Wrote {output_stream.tell()} bytes to the output stream')


def load_model(model_save_path):
    return load(model_save_path)


def load_label_encoders(encoder_save_path):
    return load(encoder_save_path)

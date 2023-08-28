import os
import pandas as pd

from src.preprocessing import preprocess_data_add_unknown
from src.training import train_and_save_model

def train_on_all_files_in_folder(input_folder_path, model_save_path="models/random_forest_model.pkl", encoder_save_path="models/label_encoders.pkl"):
    # List all CSV files in the folder
    csv_files = [f for f in os.listdir(input_folder_path) if f.endswith('.csv')]

    # Load and concatenate all CSV files
    data_frames = [pd.read_csv(os.path.join(input_folder_path, csv_file), encoding='shift-jis') for csv_file in csv_files]
    combined_data = pd.concat(data_frames, ignore_index=True)

    # Preprocess data
    preprocessed_data, label_encoders = preprocess_data_add_unknown(combined_data)
    X_train = preprocessed_data.drop(columns=["割り勘対象"])
    y_train = preprocessed_data["割り勘対象"]

    # Train and save the model
    train_and_save_model(X_train, y_train, label_encoders, model_save_path, encoder_save_path)

# Example usage:
# train_on_all_files_in_folder("path_to_input_folder")

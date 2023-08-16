import os
import pandas as pd
from joblib import load

from src.data_collection import load_data
from src.preprocessing import preprocess_data_handle_unseen
from src.inference import predict

def process_folder_for_inference(input_folder_path, output_folder_path, model_save_path="models/random_forest_model.pkl", encoder_save_path="models/label_encoders.pkl"):
    # List all CSV files in the folder
    csv_files = [f for f in os.listdir(input_folder_path) if f.endswith('.csv')]

    # Load the model and label encoders
    clf = load(model_save_path)
    label_encoders = load(encoder_save_path)

    # Process each CSV file
    for csv_file in csv_files:
        # Load data
        file_path = os.path.join(input_folder_path, csv_file)
        data = load_data(file_path)

        # Preprocess data
        preprocessed_data = preprocess_data_handle_unseen(data, label_encoders)

        # Predict
        predictions = predict(clf, preprocessed_data)

        # Add predictions to original data
        data['予測_割り勘対象'] = predictions

        # Save to the output folder
        output_file_path = os.path.join(output_folder_path, "predicted_" + csv_file)
        data.to_csv(output_file_path, index=False, encoding="SHIFT_JIS")

# Example usage:
# process_folder_for_inference("TestData", "PredictedData")

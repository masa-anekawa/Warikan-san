from joblib import load
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

def preprocess_data_add_unknown(data):
    data_cleaned = data.drop(columns=["計算対象", "日付", "ID", "メモ"])
    data_cleaned.fillna("unknown", inplace=True)

    le_dict = {}
    for col in data_cleaned.columns:
        if data_cleaned[col].dtype == 'object':
            le = LabelEncoder()
            # Add 'unknown' to each category
            data_cleaned[col] = data_cleaned[col].astype(str)
            le.fit(data_cleaned[col].append(pd.Series(["unknown"])))
            data_cleaned[col] = le.transform(data_cleaned[col])
            le_dict[col] = le

    return data_cleaned, le_dict

def preprocess_data_handle_unseen(data, label_encoders):
    data_cleaned = data.drop(columns=["計算対象", "日付", "ID", "メモ"])
    data_cleaned.fillna("unknown", inplace=True)

    for col in data_cleaned.columns:
        if col in label_encoders:
            # Set unseen categories to 'unknown'
            unseen_mask = ~data_cleaned[col].isin(label_encoders[col].classes_)
            data_cleaned.loc[unseen_mask, col] = "unknown"
            data_cleaned[col] = label_encoders[col].transform(data_cleaned[col])

    return data_cleaned

# Load the model
clf = joblib.load('random_forest_model.pkl')

# Example usage:
# train_data = pd.read_csv("path_to_train_data.csv", encoding="SHIFT_JIS")
# preprocessed_train_data, label_encoders = preprocess_data_add_unknown(train_data)
# X_train = preprocessed_train_data.drop(columns=["割り勘対象"])
# y_train = preprocessed_train_data["割り勘対象"]
# clf.fit(X_train, y_train)

# test_data = pd.read_csv("path_to_test_data.csv", encoding="SHIFT_JIS")
# preprocessed_test_data = preprocess_data_handle_unseen(test_data, label_encoders)
# predictions = clf.predict(preprocessed_test_data)

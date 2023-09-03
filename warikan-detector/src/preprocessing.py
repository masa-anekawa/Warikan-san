import pandas as pd
from joblib import dump, load
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def preprocess_data_add_unknown(data) -> tuple[pd.DataFrame, dict[str, LabelEncoder]]:
    data_cleaned: pd.DataFrame = data.drop(columns=["計算対象", "日付", "ID", "メモ"])
    data_cleaned.fillna("unknown", inplace=True)

    # Add text-based features
    data_cleaned: pd.DataFrame = extract_text_features(data_cleaned)

    le_dict: dict[str, LabelEncoder] = {}
    for col in data_cleaned.columns:
        if data_cleaned[col].dtype == 'object':
            le = LabelEncoder()
            # Using pd.concat instead of append for Series
            le.fit(pd.concat([data_cleaned[col], pd.Series(["unknown"])]))
            data_cleaned[col] = le.transform(data_cleaned[col])
            le_dict[col] = le

    return data_cleaned, le_dict

def extract_text_features(data, column_name="内容", n_features=1000) -> pd.DataFrame:
    # Initialize the TF-IDF vectorizer
    vectorizer = TfidfVectorizer(max_features=n_features)

    # Fit and transform the data
    tfidf_features = vectorizer.fit_transform(data[column_name].fillna('')).toarray()
    # print(vectorizer.get_feature_names_out())
    dump(vectorizer, "models/tfidf_vectorizer.pkl")

    # Create feature names
    feature_names = [f"{column_name}_tfidf_{i}" for i in range(n_features)]

    df_tfidf = pd.DataFrame(tfidf_features, columns=feature_names)

    # Add the TF-IDF features to the original dataframe
    data_with_features = data.copy()
    pd.concat([data_with_features, df_tfidf], axis=1)

    return data_with_features

def add_text_features(data: pd.DataFrame, column_name="内容", n_features=1000) -> pd.DataFrame:
    # Initialize the TF-IDF vectorizer
    vectorizer: TfidfVectorizer = load("models/tfidf_vectorizer.pkl")

    # Fit and transform the data
    tfidf_features = vectorizer.transform(data[column_name].fillna('')).toarray()
    # print(vectorizer.get_feature_names_out())

    # Create feature names
    feature_names = [f"{column_name}_tfidf_{i}" for i in range(n_features)]

    df_tfidf = pd.DataFrame(tfidf_features, columns=feature_names)

    # Add the TF-IDF features to the original dataframe
    data_with_features = data.copy()
    pd.concat([data_with_features, df_tfidf], axis=1)
    return data_with_features

def preprocess_data_handle_unseen(data: pd.DataFrame, label_encoders) -> pd.DataFrame:
    data_cleaned = data.drop(columns=["計算対象", "日付", "ID", "メモ"])
    data_cleaned.fillna("unknown", inplace=True)

    # Add text-based features
    data_cleaned = add_text_features(data_cleaned)

    count = 0
    for col in data_cleaned.columns:
        if col in label_encoders and data_cleaned[col].dtype == 'object':
            # Set unseen categories to 'unknown'
            unseen_mask = ~data_cleaned[col].astype(str).isin(label_encoders[col].classes_)
            data_cleaned.loc[unseen_mask, col] = "unknown"
            data_cleaned[col] = label_encoders[col].transform(data_cleaned[col].astype(str))
            count += 1
    logger.info(f"{count} label(s) encoded in {data_cleaned.shape[1]} columns")

    return data_cleaned

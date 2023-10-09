import pandas as pd
from joblib import dump, load
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def preprocess_data_add_unknown(data) -> tuple[pd.DataFrame, dict[str, LabelEncoder]]:
    y = data["割り勘対象"]
    data_cleaned = data.drop(columns=["計算対象", "日付", "ID", "メモ", "割り勘対象"])
    data_cleaned.fillna("unknown", inplace=True)

    # Add text-based features
    data_with_text_features: pd.DataFrame = extract_text_features(data_cleaned)

    # Concat previous and next row, renaming columns so that they can be distinguished
    data_convoluted = pd.concat([data_with_text_features.shift(1).add_suffix("_prev"), data_with_text_features, data_with_text_features.shift(-1).add_suffix("_next")], axis=1)

    le_dict: dict[str, LabelEncoder] = {}
    for col in data_convoluted.columns:
        if data_convoluted[col].dtype == 'object':
            le = LabelEncoder()
            # Using pd.concat instead of append for Series
            le.fit(pd.concat([data_convoluted[col], pd.Series(["unknown"])]))
            data_convoluted[col] = le.transform(data_convoluted[col])
            le_dict[col] = le

    return pd.concat([data_convoluted, y], axis=1), le_dict

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
    data_with_features = pd.concat([data_with_features, df_tfidf], axis=1)

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
    data_with_features = pd.concat([data_with_features, df_tfidf], axis=1)

    return data_with_features

def preprocess_data_handle_unseen(data: pd.DataFrame, label_encoders) -> pd.DataFrame:
    data_cleaned = data.drop(columns=["計算対象", "日付", "ID", "メモ"])
    data_cleaned.fillna("unknown", inplace=True)

    # Add text-based features
    data_with_text_features = add_text_features(data_cleaned)

    data_convoluted = pd.concat([data_with_text_features.shift(1).add_suffix("_prev"), data_with_text_features, data_with_text_features.shift(-1).add_suffix("_next")], axis=1)

    count = 0
    for col in data_convoluted.columns:
        if col in label_encoders and data_convoluted[col].dtype == 'object':
            # Set unseen categories to 'unknown'
            unseen_mask = ~data_convoluted[col].astype(str).isin(label_encoders[col].classes_)
            data_convoluted.loc[unseen_mask, col] = "unknown"
            data_convoluted[col] = label_encoders[col].transform(data_convoluted[col].astype(str))
            count += 1
    logger.info(f"{count} label(s) encoded in {data_convoluted.shape[1]} columns")

    return data_convoluted

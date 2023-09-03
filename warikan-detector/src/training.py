from abc import ABC, abstractmethod
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from joblib import dump
import numpy as np

class WarikanClassifier(ABC):
    @abstractmethod
    def predict(self, X) -> np.ndarray:
        pass


WarikanClassifier.register(XGBClassifier)
WarikanClassifier.register(RandomForestClassifier)

def train_and_save_model(X_train, y_train, label_encoders, model_path="random_forest_model.pkl", encoder_path="label_encoders.pkl") -> WarikanClassifier:
    # clf = RandomForestClassifier(n_estimators=10000, class_weight='balanced', random_state=42)

    # Initialize the XGBoost classifier
    clf = XGBClassifier(
        objective='binary:logistic',  # Binary classification problem
        eval_metric='logloss',        # Logarithmic loss metric
        use_label_encoder=False,      # Avoid a warning related to deprecation
    )
    clf.fit(X_train, y_train)

    # Save the model and label encoders
    dump(clf, model_path)
    dump(label_encoders, encoder_path)

    return clf
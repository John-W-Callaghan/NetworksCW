import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os

class AnomalyDetector:
    def __init__(self):
        # Now using three dimensions for better accuracy
        self.feature_names = ['vote_time', 'submission_speed', 'session_entropy']
        self.model = IsolationForest(contamination=0.1, random_state=42)
        
    def train(self, data):
        # Training on the 3D feature set
        self.model.fit(data[self.feature_names])
        # SAVE THE MODEL TO THE FOLDER
        if not os.path.exists('models'):
            os.makedirs('models')
        joblib.dump(self.model, 'models/isolation_forest.pkl')
        print("✅ AI Model saved to models/isolation_forest.pkl")
        
    def detect(self, vote_features):
        # vote_features should now be a list of 3 values
        df_features = pd.DataFrame([vote_features], columns=self.feature_names)
        prediction = self.model.predict(df_features)
        return "ANOMALY" if prediction[0] == -1 else "NORMAL"
import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import random

MODEL_PATH = "model.pkl"
clf = None

def load_or_train_dummy_model():
    """
    Loads model.pkl if it exists. Otherwise, trains a dummy Random Forest model
    so the application works out-of-the-box.
    """
    global clf
    if os.path.exists(MODEL_PATH):
        try:
            clf = joblib.load(MODEL_PATH)
            print("Loaded existing model.pkl")
            return
        except Exception as e:
            print(f"Could not load model.pkl: {e}. Training new dummy model.")
    
    # Train dummy model
    print("Training dummy Random Forest model...")
    # Features: [url_length, num_dots, has_at, has_hyphen_in_domain, is_https, num_subdomains]
    # Phishing typically has: longer URL, more dots, has @, has hyphen, no HTTPS, more subdomains
    
    X_dummy = []
    y_dummy = []
    
    # Generate 1000 synthetic legitimate cases
    for _ in range(1000):
        length = random.randint(15, 45)
        dots = random.randint(1, 2)
        at = 0
        hyphen = random.choice([0, 1])
        https = 1
        subd = random.randint(1, 2)
        X_dummy.append([length, dots, at, hyphen, https, subd])
        y_dummy.append(0) # 0 = Legitimate
        
    # Generate 1000 synthetic phishing cases
    for _ in range(1000):
        length = random.randint(50, 150)
        dots = random.randint(3, 5)
        at = random.choice([0, 1])
        hyphen = random.choice([0, 1])
        https = random.choice([0, 1])
        subd = random.randint(3, 6)
        X_dummy.append([length, dots, at, hyphen, https, subd])
        y_dummy.append(1) # 1 = Phishing
        
    clf = RandomForestClassifier(n_estimators=50, random_state=42)
    clf.fit(X_dummy, y_dummy)
    joblib.dump(clf, MODEL_PATH)
    print("Dummy model trained and saved as model.pkl")

def predict(features):
    global clf
    if clf is None:
        load_or_train_dummy_model()
        
    prediction = clf.predict(features)[0]
    probability = clf.predict_proba(features)[0][prediction]
    
    # Map 0 -> Legitimate, 1 -> Phishing
    label = "Phishing" if prediction == 1 else "Legitimate"
    
    return {
        "class": label,
        "probability": float(probability)
    }

def get_model():
    global clf
    if clf is None:
        load_or_train_dummy_model()
    return clf

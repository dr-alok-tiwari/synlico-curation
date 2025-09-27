import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import joblib, pathlib

df = pd.read_csv("../data/tech_training.csv")
X_train, X_test, y_train, y_test = train_test_split(df["text"], df["label"], test_size=0.2, random_state=42, stratify=df["label"])

pipe = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1,2), min_df=1, max_features=50000)),
    ("clf", LogisticRegression(max_iter=300))
])
pipe.fit(X_train, y_train)
print(classification_report(y_test, pipe.predict(X_test)))
pathlib.Path("../models").mkdir(exist_ok=True)
joblib.dump(pipe, "../models/tech_tag_clf.joblib")
print("Saved model to ../models/tech_tag_clf.joblib")

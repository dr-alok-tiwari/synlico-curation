import os, joblib
MODEL_PATH = "models/tech_tag_clf.joblib"

def ml_infer_tech(text: str):
    if not os.path.exists(MODEL_PATH):
        return None
    pipe = joblib.load(MODEL_PATH)
    return pipe.predict([text])[0]

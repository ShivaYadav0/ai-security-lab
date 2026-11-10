import joblib
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
model = joblib.load("spam_model.joblib")


class Message(BaseModel):
    text: str


@app.post("/predict")
def predict(msg: Message):
    label = model.predict([msg.text])[0]
    confidence = float(model.predict_proba([msg.text]).max())
    return {"label": label, "confidence": round(confidence, 3)}

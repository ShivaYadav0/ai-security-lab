import os
import secrets
import time
from collections import defaultdict, deque

import joblib
from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    raise SystemExit("Set the API_KEY environment variable first")

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
model = joblib.load("spam_model.joblib")

WINDOW_SECONDS = 60
MAX_REQUESTS = 10
recent = defaultdict(deque)


class Message(BaseModel):
    text: str = Field(max_length=1000)


def check_key(x_api_key: str = Header(default="")):
    if not secrets.compare_digest(x_api_key.encode(), API_KEY.encode()):
        raise HTTPException(status_code=401, detail="invalid or missing API key")
    return x_api_key


def rate_limit(key: str = Depends(check_key)):
    now = time.time()
    calls = recent[key]
    while calls and now - calls[0] > WINDOW_SECONDS:
        calls.popleft()
    if len(calls) >= MAX_REQUESTS:
        raise HTTPException(status_code=429, detail="too many requests")
    calls.append(now)


@app.post("/predict", dependencies=[Depends(rate_limit)])
def predict(msg: Message):
    return {"label": model.predict([msg.text])[0]}

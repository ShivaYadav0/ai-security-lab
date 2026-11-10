import hashlib, json, sys
import mlflow

mlflow.set_tracking_uri("http://127.0.0.1:5000")
MODEL_URI = "models:/spam-classifier/1"

def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

approved = json.load(open("approved_hashes.json"))[MODEL_URI]
local_dir = mlflow.artifacts.download_artifacts(artifact_uri=MODEL_URI)
actual = sha256_of(f"{local_dir}/model.pkl")

if actual != approved:
    sys.exit(f"REFUSING TO LOAD: hash mismatch\n  approved: {approved}\n  actual:   {actual}")

model = mlflow.sklearn.load_model(MODEL_URI)
print("Hash OK. Prediction:", model.predict(["win a free prize now"])[0])

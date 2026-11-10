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

local_dir = mlflow.artifacts.download_artifacts(artifact_uri=MODEL_URI)
digest = sha256_of(f"{local_dir}/model.pkl")
with open("approved_hashes.json", "w") as f:
    json.dump({MODEL_URI: digest}, f, indent=2)
print("Approved", MODEL_URI, "->", digest)

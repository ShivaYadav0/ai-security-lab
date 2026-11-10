import mlflow
mlflow.set_tracking_uri("http://127.0.0.1:5000")
model = mlflow.sklearn.load_model("models:/spam-classifier/1")
print("Loaded. Prediction:", model.predict(["win a free prize now"])[0])

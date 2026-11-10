import mlflow
from mlflow.models import infer_signature
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("spam-classifier")

texts = ["win free money now", "claim your prize today", "free entry click here",
         "meeting at 10am tomorrow", "lunch with the team", "please review the report"]
labels = ["spam", "spam", "spam", "ham", "ham", "ham"]

model = make_pipeline(TfidfVectorizer(), LogisticRegression())
model.fit(texts, labels)

with mlflow.start_run() as run:
    mlflow.log_param("model_type", "tfidf+logreg")
    mlflow.log_metric("train_accuracy", model.score(texts, labels))
    info = mlflow.sklearn.log_model(
        model, name="model",
        registered_model_name="spam-classifier",
        signature=infer_signature(texts, model.predict(texts)),
        serialization_format="cloudpickle",
    )
    print("run id:", run.info.run_id)
    print("model uri:", info.model_uri)

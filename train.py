"""Train the placement predictor, log everything to MLflow, save model for serving."""
import argparse
import joblib
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split

FEATURES = ["cgpa", "dsa_problems", "projects", "internships", "communication", "backlogs"]

parser = argparse.ArgumentParser()
parser.add_argument("--n_estimators", type=int, default=100)
parser.add_argument("--max_depth", type=int, default=6)
args = parser.parse_args()

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("placement-predictor")

df = pd.read_csv("data/placement.csv")
X, y = df[FEATURES], df["placed"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

with mlflow.start_run():
    model = RandomForestClassifier(
        n_estimators=args.n_estimators, max_depth=args.max_depth, random_state=42
    )
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    f1 = f1_score(y_test, preds)

    mlflow.log_params({"n_estimators": args.n_estimators, "max_depth": args.max_depth})
    mlflow.log_metrics({"accuracy": acc, "f1": f1})
    mlflow.sklearn.log_model(model, artifact_path="model",
                             skops_trusted_types=["sklearn.tree._tree.Tree"])

    joblib.dump(model, "model/model.joblib")
    print(f"n_estimators={args.n_estimators} max_depth={args.max_depth} "
          f"-> accuracy={acc:.3f} f1={f1:.3f}")

# MLOps Starter: Placement Chance Predictor

Pipeline: **Git -> MLflow -> FastAPI -> Docker -> GitHub Actions -> AWS EC2 (next session)**

## Setup
```bash
git clone <REPO_URL>
cd mlops-starter
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Step 1: Train and track experiments
Run three times with different settings:
```bash
python train.py --n_estimators 1 --max_depth 1
python train.py --n_estimators 5 --max_depth 2
python train.py --n_estimators 100 --max_depth 6
```
Open the MLflow UI and compare runs:
```bash
mlflow ui --backend-store-uri sqlite:///mlflow.db
```
Go to http://127.0.0.1:5000

## Step 2: Serve the model as an API
```bash
uvicorn app:app --reload
```
Open http://127.0.0.1:8000 (the web app) or /docs (the API explorer). Enter your own numbers!

## Step 3: Run tests
```bash
python -m pytest -q
```

## Step 4: Docker (trainer demo, optional for you)
```bash
docker build -t placement-api .
docker run -p 8000:8000 placement-api
```

## Step 5: CI
Push to GitHub, open the **Actions** tab, and watch the tests run.

## Step 6: Deploy (next session)
We deploy this same container to AWS EC2.

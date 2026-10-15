# Every file in this repo, explained

| File | What it is | When students meet it |
|---|---|---|
| `data/generate_data.py` | Script that creates the fake dataset (2000 students). Run once; the CSV is already included. | Session 1 (show only) |
| `data/placement.csv` | The training data: CGPA, DSA problems solved, projects, internships, communication, backlogs, and whether the student was placed. **Synthetic, not real.** | Session 1 |
| `train.py` | Trains a Random Forest, logs parameters and metrics to MLflow, and saves the model to `model/model.joblib`. Takes `--n_estimators` and `--max_depth` so students can experiment. | Session 1 (main hands-on) |
| `model/model.joblib` | The trained model file. `app.py` loads it. A baseline is committed so the repo works on day one; `train.py` overwrites it. | Session 1-2 |
| `app.py` | The FastAPI web service. `/` shows the web page, `/predict` returns the placement chance and tips, `/health` says if it's alive. Validates inputs. | Session 2 |
| `static/index.html` | The simple web page where students type their own numbers. | Session 2 (the fun part) |
| `tests/test_app.py` | 4 automated tests: health check, home page loads, strong profile beats weak profile, bad input rejected. | Session 2 (CI) |
| `Dockerfile` | Recipe to package the app, model and web page into one container. | Session 2 |
| `.github/workflows/ci.yml` | GitHub Actions: on every push, install, train, and run the tests. Green tick or red cross. | Session 2 |
| `requirements.txt` | Libraries for training and testing (includes MLflow and pytest). | Setup |
| `requirements-serve.txt` | Smaller list for the container. No MLflow, so the image is lighter. | Docker |
| `.gitignore` | Tells Git to skip `venv/`, `mlruns/`, `mlflow.db`. | Git demo |
| `.dockerignore` | Keeps junk out of the Docker image. | Docker |
| `README.md` | Student instructions, step by step. | Students |
| `TRAINER_GUIDE.md` | Your private run sheet (checklist, live steps, EC2). | You only |
| `MLFLOW_GUIDE.md` | MLflow explained, with exact steps. | You and students |
| `FILES_EXPLAINED.md` | This file. | You |

**Auto-created when you run things (not committed):** `mlflow.db` (MLflow's database), `mlruns/` (saved model artifacts), `venv/` (Python environment), `__pycache__/`.

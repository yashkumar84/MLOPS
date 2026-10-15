# MLflow: what it is and how to use it

## What is MLflow?
An open-source tool that **records your ML experiments**: which settings you used, what results you got, and the model that came out. Without it, you rely on file names like `final_v2_REAL.pkl` and memory. With it, every run is saved and comparable in a web page.

Analogy: a fitness app for your models. Each training run is a workout. MLflow logs the details so you can see which one actually made progress.

## The four things you log
| Concept | Meaning | In `train.py` |
|---|---|---|
| **Experiment** | A folder of related runs | `mlflow.set_experiment("placement-predictor")` |
| **Run** | One training attempt | `with mlflow.start_run():` |
| **Parameters** | Settings you chose | `mlflow.log_params({...})` |
| **Metrics** | Results you measured | `mlflow.log_metrics({...})` |
| **Artifacts / Model** | Saved files, including the model | `mlflow.sklearn.log_model(...)` |

## Step by step

**1. Install** (already in requirements.txt)
```bash
pip install -r requirements.txt
```

**2. Run training three times with different settings**
```bash
python train.py --n_estimators 1   --max_depth 1     # accuracy ~0.635
python train.py --n_estimators 5   --max_depth 2     # accuracy ~0.748
python train.py --n_estimators 100 --max_depth 6     # accuracy ~0.820
```
Each run creates a record in `mlflow.db` (and files in `mlruns/`).

**3. Open the MLflow UI**
```bash
mlflow ui --backend-store-uri sqlite:///mlflow.db
```
Open http://127.0.0.1:5000 in the browser. Leave the terminal running. Press Ctrl+C to stop.

**4. Explore the UI**
1. Click the experiment **placement-predictor** on the left.
2. You see a table with one row per run, with parameters and metrics as columns.
3. Click the **accuracy** column header to sort, and find the best run.
4. Tick 2-3 runs and click **Compare** to see them side by side (charts are useful for projecting).
5. Click one run's name to open its page: parameters, metrics, and under **Artifacts** the saved model.

**5. Decide which model ships**
The run with the best accuracy and F1 wins. Because `train.py` always saves to `model/model.joblib`, **re-run the winning settings last** so that file holds the best model, then commit it:
```bash
python train.py --n_estimators 100 --max_depth 6
git add model/model.joblib
git commit -m "Ship best model"
```

## Teaching tips
- Ask students to predict which run will win before showing the table.
- Point out the 100/6 vs 300/12 case: more trees and depth don't always help (try it: both give 0.820).
- Make the point: "If your teammate asks which settings gave 82%, this is how you answer in 5 seconds."

## Common problems
| Problem | Fix |
|---|---|
| UI shows no runs | You started `mlflow ui` in a different folder or forgot `--backend-store-uri sqlite:///mlflow.db`. Run it from the repo folder. |
| `Address already in use` | Another MLflow UI is running. Add `--port 5001`. |
| SQLAlchemy / import error on install | Use the pinned versions in `requirements.txt`. |

## What's beyond this session
MLflow can also register models with versions and stages (Model Registry), serve models directly, and run on a shared server for teams. Mention these, but don't teach them in 4 hours.

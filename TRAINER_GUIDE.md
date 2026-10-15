# Trainer Guide (for you only; don't give this to students)

## A. Before-work checklist

### You (do in this order)
1. Create a GitHub repo `mlops-starter`, push this folder. Make it **public**.
2. Fresh-clone it into a new folder, follow README start to finish. Fix anything that breaks.
3. Run `docker build` and `docker run` once on your machine.
4. Push a commit, confirm the GitHub Actions run is green.
5. Do a full EC2 dry run (Section D) with a throwaway instance. Terminate it after.
6. Make a backup ZIP of the repo (USB/Drive) for bad Wi-Fi.
7. Enable GitHub Codespaces on the repo as fallback for broken laptops.

### Students (send 2-3 days before)
Subject: Pre-work for MLOps session (15 min, please do it!)
- Install Python 3.10+ (tick "Add to PATH" on Windows)
- Install Git and VS Code
- Create a GitHub account
- Run `python --version` and `git --version`, and reply with a screenshot
- Create a free AWS account (needs a card for verification; start early, activation can take a day)
- Optional: Docker Desktop (skip if the laptop is slow)

## B. Session 1: what to do in front of them

1. **Hook (10 min)**: the "95% accuracy, but who uses it?" story. No slides needed.
2. **Show the repo (10 min)**: walk through the 5 key files: `train.py`, `app.py`, `Dockerfile`, `ci.yml`, `tests/`. Say: "By the end of Session 2, all of this is live on the internet."
3. **Setup together (15 min)**: clone, venv, `pip install -r requirements.txt`. Walk the room while it installs.
4. **Explain `train.py` (10 min)**: only point at the MLflow lines: `log_params`, `log_metrics`, `log_model`.
5. **Hands-on (25 min)**: everyone runs the 3 training commands from the README. Expected accuracy: 0.635, 0.748, 0.820.
6. **MLflow UI (15 min)**: `mlflow ui --backend-store-uri sqlite:///mlflow.db`. Compare runs, sort by accuracy. Ask: "Which run goes to production, and why?"
7. **Git habit (10 min)**: `git add . && git commit -m "best model" && git push`.
8. Recap. Homework: run `uvicorn app:app --reload` and open `/docs`.

## C. Session 2 flow

1. Recap quiz (5-10 min).
2. **FastAPI**: run `uvicorn`, open `/` (the web app), let students type their own numbers, then open `/docs` and send an invalid value (CGPA 15 gives 422). Explain validation.
3. **Tests + CI**: `python -m pytest -q`, push, show the green tick in the Actions tab. Then deliberately break a test, push, and show the red cross.
4. **Docker** (demo from your laptop): `docker build -t placement-api .`, `docker run -p 8000:8000 placement-api`.
5. **EC2 deploy** (Section D), 45 min.
6. Monitoring concepts, wrap-up, roadmap.

## D. EC2 deployment steps

**Console (once per student):**
1. EC2 -> Launch instance -> Ubuntu 22.04/24.04, instance type `t2.micro` or `t3.micro` (whichever is free-tier eligible on their account).
2. Create a key pair and download the `.pem` file.
3. Security group inbound rules: SSH (22) from My IP, Custom TCP **8000** from Anywhere (0.0.0.0/0, demo only).
4. Launch, then copy the **Public IPv4 address**.

**SSH in:**
```bash
chmod 400 key.pem          # Mac/Linux
ssh -i key.pem ubuntu@<PUBLIC_IP>
```
(Windows: VS Code Remote-SSH, PuTTY, or the EC2 "Connect" button in the browser. The browser option is the least painful for a class.)

**On the server:**
```bash
sudo apt update && sudo apt install -y docker.io git
sudo systemctl enable --now docker
git clone <THEIR_REPO_URL>
cd mlops-starter
sudo docker build -t placement-api .
sudo docker run -d --restart unless-stopped -p 8000:8000 placement-api
```

**Verify:** open `http://<PUBLIC_IP>:8000` in the browser, or:
```bash
curl -X POST http://<PUBLIC_IP>:8000/predict -H "Content-Type: application/json" \
  -d '{"cgpa":7.5,"dsa_problems":120,"projects":2,"internships":1,"communication":7,"backlogs":0}'
```

**Cleanup (tell them!):** terminate the instance after class so there are no surprise bills. Check the AWS Free Tier terms on your students' accounts, since they change.

**Joke:** "AWS bills are like ex-partners. Forgetting to terminate means you'll hear from them again."

## E. Risks
- Free tier / card verification is the biggest blocker. Plan a fallback: you deploy one shared EC2 and students push to a Space, or work in pairs on one account.
- Docker build on a t2.micro (1 GB RAM) takes a couple of minutes. Start it, then explain while it runs.
- If a student's push or clone fails, give them the backup ZIP.

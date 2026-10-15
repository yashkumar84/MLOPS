from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

STRONG = {"cgpa": 9.0, "dsa_problems": 300, "projects": 5, "internships": 2,
          "communication": 8, "backlogs": 0}
WEAK = {"cgpa": 5.5, "dsa_problems": 10, "projects": 0, "internships": 0,
        "communication": 3, "backlogs": 4}


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_home_page_loads():
    r = client.get("/")
    assert r.status_code == 200 and "Placement" in r.text


def test_strong_beats_weak():
    strong = client.post("/predict", json=STRONG).json()["placement_chance_percent"]
    weak = client.post("/predict", json=WEAK).json()["placement_chance_percent"]
    assert strong > 70 and weak < 30 and strong > weak


def test_bad_input_rejected():
    bad = {**STRONG, "cgpa": 15}
    assert client.post("/predict", json=bad).status_code == 422

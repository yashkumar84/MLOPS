"""Generate a synthetic student-placement dataset (for learning only, NOT real data)."""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
N = 2000

cgpa = np.clip(rng.normal(7.2, 1.0, N), 4.5, 10).round(2)
dsa_problems = np.clip(rng.gamma(2.0, 45, N), 0, 600).astype(int)
projects = np.clip(rng.poisson(2.0, N), 0, 8)
internships = np.clip(rng.poisson(0.8, N), 0, 3)
communication = np.clip(rng.normal(6, 2, N), 1, 10).round(1)
backlogs = np.clip(rng.poisson(0.6, N), 0, 6)

score = (
    1.1 * (cgpa - 7.0)
    + 0.012 * (dsa_problems - 90)
    + 0.35 * (projects - 2)
    + 0.6 * internships
    + 0.25 * (communication - 6)
    - 0.8 * backlogs
    + rng.normal(0, 1.0, N)
)
placed = (score > 0.3).astype(int)

df = pd.DataFrame({
    "cgpa": cgpa, "dsa_problems": dsa_problems, "projects": projects,
    "internships": internships, "communication": communication,
    "backlogs": backlogs, "placed": placed,
})
df.to_csv("data/placement.csv", index=False)
print(df.shape, "placed rate:", round(placed.mean(), 3))

from pathlib import Path
import py_compile
import json
import sys

ROOT = Path(__file__).resolve().parent.parent

REQUIRED = [
    "backend/app.py",
    "backend/models.py",
    "backend/services/sleep_calculator.py",
    "backend/services/correlation_engine.py",
    "backend/services/recommendation_engine.py",
    "frontend/src/App.vue",
    "frontend/src/views/DashboardView.vue",
    "frontend/src/views/EntryView.vue",
    "frontend/src/views/TrendsView.vue",
    "frontend/src/views/InsightsView.vue",
    "frontend/src/views/RecommendationsView.vue",
    "frontend/src/views/GoalsView.vue",
    "frontend/package.json",
    "README.md",
]

missing = [item for item in REQUIRED if not (ROOT / item).exists()]
if missing:
    print("Missing files:", *missing, sep="\n- ")
    raise SystemExit(1)

for path in (ROOT / "backend").rglob("*.py"):
    py_compile.compile(str(path), doraise=True)

package = json.loads((ROOT / "frontend/package.json").read_text(encoding="utf-8"))
assert "vue" in package["dependencies"]
assert "chart.js" in package["dependencies"]
assert "vite" in package["devDependencies"]

print("Project structure verified.")
print("Python source files compile successfully.")
print("Frontend package manifest includes Vue, Chart.js, and Vite.")

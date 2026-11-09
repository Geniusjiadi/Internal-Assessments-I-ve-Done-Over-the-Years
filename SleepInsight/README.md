# SleepInsight

SleepInsight is a Vue 3 + Python/Flask + SQLite web application for recording sleep and lifestyle behaviour, analysing patterns, calculating explainable scores and correlations, ranking rule-based recommendations, and tracking measurable goals.

## Core features

- Sleep CRUD with cross-midnight duration calculation and input validation
- Caffeine, exercise, and screen-use recording
- 7-day and 30-day rolling comparisons
- Sleep regularity analysis with midnight normalization
- Weekday/weekend comparison and social-jet-lag estimate
- Explainable weighted sleep score
- Student-implemented Spearman rank correlation with tied-rank handling
- Sample-size confidence states
- Pattern detection
- Rule-based recommendation ranking
- Explainable "Why am I seeing this?" evidence
- Goal progress and adaptive target suggestions
- Vue dashboard, trends, insights, recommendations, goals, and responsive design
- Local SQLite persistence

## 1. Create a Python environment

```bash
python -m venv .venv
```

Activate it, then:

```bash
pip install -r requirements.txt
```

## 2. Seed demonstration data (optional but recommended)

```bash
python -m backend.seed
```

## 3. Run backend

```bash
python run.py
```

Backend: `http://127.0.0.1:5000`

Health check: `http://127.0.0.1:5000/api/health`

## 4. Run frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend: `http://127.0.0.1:5173`

The Vite development server proxies `/api` to Flask.

## 5. Run progressive tests

```bash
python scripts/test_progressive.py
```

Or:

```bash
python -m unittest discover -s tests -v
```

After installing frontend packages:

```bash
cd frontend
npm run build
```

## Important IA note

Treat this project as a development scaffold, not as unexplained submission-ready code. You should understand, adapt, test, document, and be able to explain every algorithm and design decision you keep. Record any external or AI assistance according to your teacher's and IB's current academic-integrity requirements.

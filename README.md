# CivicSage

**Exasol-powered civic intelligence for finding hidden public-service blind spots.**

CivicSage is an AI-driven platform that analyzes large-scale public-service data to surface problems that standard dashboards miss. It combines resolution performance, case aging, backlog volume, citizen signals, and AI-assisted investigation to reveal where official metrics may not reflect the real citizen experience.

> Turns millions of operational records into explainable civic blind spots.

---

## Table of Contents

- [The Problem](#the-problem)
- [What CivicSage Does](#what-civicsage-does)
- [Why Exasol](#why-exasol)
- [Risk Engine](#risk-engine)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [API Reference](#api-reference)
- [Getting Started](#getting-started)
- [Demo Flow](#demo-flow)
- [Design Philosophy](#design-philosophy)
- [Disclaimer](#disclaimer)

---

## The Problem

Traditional public-service dashboards answer *"how many cases were resolved?"* — but not *"were citizens actually helped?"*

A department can report a high resolution rate while still facing:

- Growing long-term backlogs
- Large numbers of aging cases
- Rising repeat complaints
- Poor resolution quality
- Regional performance gaps

This gap between **administrative performance** and **citizen experience** is CivicSage's core target.

## What CivicSage Does

| Capability | Description |
|---|---|
| **Operational Intelligence** | Tracks cases received/disposed, resolution rates, pending and aging cases, and historical trends. |
| **Blind-Spot Detection** | Calculates a composite risk score across departments/regions to rank where attention is needed most. |
| **AI Investigation** | Generates a brief on what's happening, why, which signals support it, and what to review next. |
| **Reality Check** | Flags contradictions, e.g. improving closure rates alongside rising repeat complaints. |
| **Evidence Chain** | Traces any insight back to its underlying data. |
| **Impact Tracking** | Compares before/after outcomes to see if an intervention actually worked. |

### Demo Scale

- **5.32M+** cases analyzed
- **124** blind spots detected

**Example blind spot — Legal Affairs:**

| Metric | Value |
|---|---|
| Resolution Rate | 76.63% |
| Pending > 1 Year | 61.13% |
| Pending > 3 Years | 67 |
| Total Pending | 2,822 |
| Risk Score | 69.97 |
| Severity | MEDIUM |

## Why Exasol

Exasol isn't just storage — it's the analytical engine. Instead of pulling the full dataset into Python for processing, CivicSage pushes the heavy computation into Exasol via SQL: normalization, weighted risk scoring, logarithmic volume scaling, severity classification, and ranking. Only the small, final result set is passed to the application layer.

```
Large Dataset → Exasol (aggregate, normalize, score, rank) → Small Result → FastAPI
```

## Risk Engine

Risk scores are calculated per department/region using a weighted model:

```
Risk Score = 0.35 × Backlog Risk
           + 0.30 × Aging Risk
           + 0.20 × Resolution Risk
           + 0.15 × Volume Score
```

| Signal | Weight | What it Measures |
|---|---:|---|
| Long-term backlog | 35% | Cases pending more than 3 years |
| Aging | 30% | Cases unresolved for more than 1 year |
| Resolution | 20% | Lower resolution rate → higher risk |
| Volume | 15% | Log-scaled case volume, so large departments aren't unfairly penalized |

**Severity thresholds:**

| Risk Score | Severity |
|---|---|
| ≥ 70 | HIGH |
| 40 – 69.99 | MEDIUM |
| < 40 | LOW |

**Pipeline:**

```
Raw KPI Data → Dataset Statistics → Normalize Signals → Weighted Score → Severity → Ranked Blind Spots
```

## Architecture

```
Civic Data
    │
    ▼
┌─────────────────────┐
│       Exasol         │  KPI analytics, aggregation, risk scoring, ranking
└──────────┬────────────┘
           ▼
┌─────────────────────┐
│       FastAPI         │  Business logic, AI investigation, evidence APIs
└──────────┬────────────┘
           ▼
┌─────────────────────┐
│    Next.js / React    │  CivicSage dashboard UI
└─────────────────────┘
```

Deployment runs on **AWS**, with Exasol and the FastAPI backend as separate services both feeding the frontend.

## Tech Stack

- **Frontend:** Next.js, React, TypeScript/JavaScript
- **Backend:** Python, FastAPI, Pandas
- **Database & Analytics:** Exasol, SQL (aggregation, scoring, ranking, normalization)
- **AI:** Investigation briefs, evidence interpretation
- **Infrastructure:** AWS, GitHub

## Project Structure

```
Exasol/
├── backend/
│   ├── app/
│   │   ├── routers/          # dashboard, blind_spots, investigations, evidence, impact_tracker
│   │   └── services/         # exasol_service, blind_spot_detector, gemini_investigator, reality_check_service
│   ├── data/
│   ├── data-pipeline/clean/
│   ├── load_exasol_data.py
│   ├── test_exasol.py
│   └── requirements.txt
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── package.json
└── README.md
```

The core analytical table is **`CIVICSAGE.DEPT_KPIS`**, queried directly by the blind-spot detection engine.

## API Reference

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Backend health check |
| GET | `/api/dashboard` | Dashboard analytics |
| GET | `/api/blind-spots` | Ranked blind spots |
| POST | `/api/reality-check` | Reality-check analysis |
| GET | `/api/investigations` | Investigation data |
| POST | `/api/investigations/{id}/review` | Human review |
| GET | `/api/evidence` | Evidence chain |
| GET | `/api/impact-tracker` | Impact comparison |

## Getting Started

### Backend

```bash
cd backend
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend runs at `http://127.0.0.1:8000`

### Frontend

```bash
cd frontend
npm install
npm run dev -- --webpack
```

Frontend runs at `http://localhost:3000`

### Environment Variables

Create `backend/.env` (use `backend/.env.example` as a template):

```bash
EXASOL_DSN=your_exasol_dsn
EXASOL_USER=your_exasol_username
EXASOL_PASSWORD=your_exasol_password
GEMINI_API_KEY=your_gemini_api_key
```

> **Security:** Never commit API keys, database passwords, AWS credentials, or other secrets. `.env` is git-ignored — only `.env.example` should be committed.

### Testing the Exasol Connection

```bash
python test_exasol.py
```

Or a quick one-liner:

```bash
python -c "from app.services.exasol_service import get_exasol_connection; c=get_exasol_connection(); print(c.execute('SELECT 1').fetchone()); c.close()"
```

Expected output: `(1,)`

### Testing the Dashboard API

```bash
# with the backend running
curl http://127.0.0.1:8000/api/dashboard
```

Example response:

```json
{
  "active_blind_spots": 124,
  "high_severity_count": 0,
  "cases_analyzed": 5320297
}
```

## Demo Flow

1. **Dashboard** — overview of cases analyzed, blind spots, high-risk areas, and trends.
2. **Blind Spots** — see departments/regions ranked by risk; select one to explore.
3. **Risk Score Breakdown** — show it's multi-signal: Backlog (35%), Aging (30%), Resolution (20%), Volume (15%).
4. **Exasol Highlight** — explain that the heavy computation runs as SQL inside Exasol, not in the app layer.
5. **Reality Check** — compare official metrics against citizen-facing signals for contradictions.
6. **AI Investigation** — generate a brief: anomaly, evidence, causes, recommended review.
7. **Evidence Chain** — trace the investigation back to supporting data.
8. **Impact Tracker** — show before/after outcomes of an intervention.

## Design Philosophy

1. **Detect, don't just display** — surface risky patterns, not just charts.
2. **Multi-signal analysis** — no single KPI drives a flag.
3. **Explainable intelligence** — every blind spot has interpretable indicators behind it.
4. **Human-in-the-loop** — AI assists investigators; it doesn't replace judgment.
5. **Evidence before action** — findings must be backed by observable data.

## Disclaimer

CivicSage is an **educational and hackathon prototype**. Datasets are synthetic and do not represent real government records, live systems, or actual citizen complaints. Risk scores are analytical indicators only, not definitive judgments about any department, region, or individual. AI-generated findings are meant to support human review and should always be validated against real evidence.

---

**Built with:** Exasol · AWS · FastAPI · Next.js · React · Python · SQL · AI

*Submitted for the Exasol AI Build Challenge 2026.*

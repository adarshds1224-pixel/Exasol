# CivicSage

## Exasol-Powered Civic Intelligence for Finding Hidden Public-Service Blind Spots

CivicSage is an AI-powered civic intelligence platform that analyzes large-scale public-service operational data to uncover problems that conventional dashboards can miss.

Instead of looking only at whether cases were closed, CivicSage looks deeper by combining resolution performance, case aging, backlog volume, citizen signals, historical trends, and AI-assisted investigation to identify where official performance may not reflect the actual citizen experience.

The core analytical workload is powered by Exasol, with risk scoring and large-scale aggregation executed directly in the database. The application layer uses FastAPI, while the interactive intelligence dashboard is built with Next.js and React.

> CivicSage turns millions of operational records into explainable civic blind spots.

---

## The Problem

Traditional public-service dashboards often answer:

> "How many cases were resolved?"

But that does not necessarily answer:

> "Were citizens actually helped?"

A department may report a high resolution rate while simultaneously experiencing:

- Increasing long-term backlogs
- Large numbers of aging cases
- Increasing repeat complaints
- Worsening follow-up behavior
- Poor resolution quality
- Regional performance disparities

This creates a blind spot between administrative performance and citizen experience.

CivicSage is designed to expose that gap.

---

## What CivicSage Does

CivicSage provides a unified intelligence layer for civic operations.

### 1. Operational Intelligence

Monitor:

- Cases received
- Cases disposed
- Resolution rates
- Pending cases
- Aging cases
- Processing performance
- Historical trends

### 2. Blind-Spot Detection

CivicSage calculates a composite risk score using multiple operational indicators.

| Signal | Weight |
|---|---:|
| Long-term backlog | 35% |
| Cases aging >1 year | 30% |
| Resolution risk | 20% |
| Pending-case volume | 15% |

This produces a ranked list of departments and regions requiring attention.

### 3. AI Investigation

Once a potential blind spot is identified, the system can generate an investigation brief to help answer:

- What is happening?
- Why might it be happening?
- Which signals support the finding?
- What evidence should be reviewed?
- What action should be considered?

### 4. Reality Check

CivicSage compares official operational performance with citizen-facing signals to identify contradictions such as:

> Improving closure rate + worsening repeat complaints

or:

> Better SLA compliance + increasing unresolved follow-ups

### 5. Evidence Chain

Investigators can trace an insight back to the underlying evidence and supporting signals.

### 6. Impact Tracking

The platform provides before-and-after comparisons to evaluate whether an intervention actually improves outcomes.

---

## Why Exasol?

Exasol is not simply used as a storage layer in CivicSage.

The analytical intelligence runs directly in Exasol.

Blind-spot detection is performed through SQL using:

- Statistical normalization
- Risk scoring
- Logarithmic volume scaling
- Weighted analytical calculations
- Severity classification
- Ranking

Instead of transferring the entire analytical dataset into Python and performing the heavy workload there, CivicSage pushes the computation into Exasol.

### Architecture

```text
                    CIVIC DATA
                        |
                        v
               +------------------+
               |      EXASOL      |
               |                  |
               | KPI Analytics    |
               | Aggregations     |
               | Risk Scoring     |
               | Ranking          |
               +--------+---------+
                        |
                        v
               +------------------+
               |     FastAPI      |
               |                  |
               | Business Logic   |
               | AI Investigation |
               | Evidence APIs    |
               +--------+---------+
                        |
                        v
               +------------------+
               |  Next.js / React |
               |                  |
               |   CivicSage UI   |
               +------------------+

Current Demo Scale

The current Exasol-backed demonstration analyzes more than:

5.32 Million Cases

The current analytical pipeline produces:

124 Detected Blind Spots

The dashboard provides:

Overall operational metrics
Ranked blind spots
Risk scores
Severity classification
Yearly operational trends
Monthly prediction vs actual analysis
Department-level indicators
Regional performance indicators
AI investigation workflows

Example blind-spot result:

Legal Affairs

Resolution Rate       76.63%
Pending >3 Years      67
Pending >1 Year       61.13%
Total Pending         2,822
Risk Score            69.97
Severity              MEDIUM
Blind-Spot Risk Engine

The analytical pipeline runs directly inside Exasol.

The system first calculates dataset-level statistics and then normalizes multiple risk indicators.

Raw KPI Data
     |
     v
Calculate Dataset Statistics
     |
     +-- Resolution range
     +-- Aging range
     +-- Backlog range
     +-- Volume range
     |
     v
Normalize Risk Signals
     |
     v
Weighted Risk Score
     |
     v
Severity Classification
     |
     v
Ranked Blind Spots
Risk Calculation

The current scoring model uses:

Risk Score =
    0.35 x Backlog Risk
  + 0.30 x Aging Risk
  + 0.20 x Resolution Risk
  + 0.15 x Volume Score
Risk Components
Long-Term Backlog Risk

Measures the relative level of cases pending for more than three years.

Aging Risk

Measures the percentage of cases that have remained unresolved for more than one year.

Resolution Risk

Lower resolution rates produce higher risk.

Volume Score

Uses logarithmic scaling so that extremely large departments do not automatically dominate the ranking simply because of their size.

Severity Classification
Risk Score >= 70       HIGH
Risk Score 40-69.99    MEDIUM
Risk Score < 40        LOW

This approach allows CivicSage to identify potential operational blind spots using multiple signals rather than relying on a single KPI.

System Architecture
                         +------------------+
                         |   CivicSage UI   |
                         | Next.js + React  |
                         +--------+---------+
                                  |
                                  |
                                  v
                         +------------------+
                         |     FastAPI      |
                         |    REST APIs     |
                         +--------+---------+
                                  |
                +-----------------+-----------------+
                |                 |                 |
                v                 v                 v
         +-------------+   +-------------+   +-------------+
         |   Exasol    |   | AI Services |   | Civic Data  |
         |             |   |             |   |             |
         | KPI Engine  |   | Investigator|   | Evidence    |
         | Risk Engine |   | Insights    |   | Signals     |
         +-------------+   +-------------+   +-------------+
Technology Stack
Frontend
Next.js
React
JavaScript / TypeScript
Dashboard visualizations
Backend
Python
FastAPI
Pandas
REST APIs
Database and Analytics
Exasol
SQL
Analytical aggregation
Risk scoring
Ranking
Data normalization
AI
AI-assisted investigation
Evidence interpretation
Investigation brief generation
Cloud and Infrastructure
AWS
Exasol deployed on AWS
GitHub
Project Structure
Exasol/
|
+-- backend/
|   |
|   +-- app/
|   |   |
|   |   +-- routers/
|   |   |   +-- dashboard.py
|   |   |   +-- blind_spots.py
|   |   |   +-- investigations.py
|   |   |   +-- evidence.py
|   |   |   +-- impact_tracker.py
|   |   |
|   |   +-- services/
|   |       +-- exasol_service.py
|   |       +-- blind_spot_detector.py
|   |       +-- gemini_investigator.py
|   |       +-- contradiction_service.py
|   |       +-- reality_check_service.py
|   |
|   +-- data/
|   |
|   +-- data-pipeline/
|   |   +-- clean/
|   |
|   +-- load_exasol_data.py
|   +-- test_exasol.py
|   +-- requirements.txt
|   +-- .env.example
|
+-- frontend/
|   |
|   +-- app/
|   +-- components/
|   +-- lib/
|   +-- public/
|   +-- package.json
|
+-- README.md
+-- push_repo.py
API

The FastAPI backend exposes the following major endpoints:

Method	Endpoint	Purpose
GET	/health	Backend health check
GET	/api/dashboard	Dashboard analytics
GET	/api/blind-spots	Ranked blind spots
POST	/api/reality-check	Reality-check analysis
GET	/api/investigations	Investigation data
POST	/api/investigations/{id}/review	Human review
GET	/api/evidence	Evidence chain
GET	/api/impact-tracker	Impact comparison
Data Pipeline

CivicSage processes structured civic-service data representing:

Operational KPIs
Citizen signals
Historical cases
Processing performance
Case aging
Resolution metrics
Regional performance
Prediction and actual trends

The data pipeline prepares analytical datasets before loading relevant KPI data into Exasol.

Source Data
     |
     v
Cleaning & Transformation
     |
     v
Analytical KPI Tables
     |
     v
Exasol
     |
     v
SQL Risk Engine
     |
     v
FastAPI
     |
     v
CivicSage Dashboard
Exasol Data Integration

The project contains a dedicated Exasol service:

backend/app/services/exasol_service.py

The service manages the connection between FastAPI and the Exasol database.

The blind-spot detector queries Exasol directly:

FastAPI
   |
   v
Exasol Service
   |
   v
CIVICSAGE.DEPT_KPIS
   |
   v
Analytical SQL
   |
   v
Risk Scores
   |
   v
Blind Spots

The primary analytical table is:

CIVICSAGE.DEPT_KPIS

This table contains department-level KPI data used by the blind-spot detection engine.

AWS + Exasol

CivicSage uses an Exasol deployment running on AWS for its analytical workload.

The architecture separates the application layer from the analytical database:

                    AWS
                     |
        +------------+------------+
        |                         |
        v                         v
   FastAPI Backend          Exasol Database
        |                         |
        |                         |
        +-----------+-------------+
                    |
                    v
              CivicSage UI

The backend connects to Exasol through environment-based configuration.

Database credentials are intentionally excluded from the repository.

Local Development
Backend

Navigate to the backend:

cd backend

Create a virtual environment:

python -m venv .venv
Windows PowerShell
.venv\Scripts\Activate.ps1
Linux/macOS
source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Start the FastAPI server:

uvicorn app.main:app --reload

The backend will be available at:

http://127.0.0.1:8000
Frontend

Navigate to the frontend:

cd frontend

Install dependencies:

npm install

Start the Next.js development server:

npm run dev -- --webpack

The frontend will be available at:

http://localhost:3000
Environment Variables

Create a local environment file:

backend/.env

Configure the required Exasol and AI credentials.

Example configuration:

EXASOL_DSN=your_exasol_dsn
EXASOL_USER=your_exasol_username
EXASOL_PASSWORD=your_exasol_password
GEMINI_API_KEY=your_gemini_api_key

Use the following file as the template:

backend/.env.example
Security

Never commit:

API keys
Database passwords
AWS credentials
Exasol credentials
Other private secrets

The repository uses .gitignore to prevent local .env files from being committed.

Testing the Exasol Connection

From the backend directory:

python test_exasol.py

A successful connection should return a valid Exasol query result.

A simple connection test can also be performed with:

python -c "from app.services.exasol_service import get_exasol_connection; c=get_exasol_connection(); print(c.execute('SELECT 1').fetchone()); c.close()"

Expected result:

(1,)
Testing the Dashboard API

Start the backend:

uvicorn app.main:app --reload

Then run:

Windows PowerShell
curl.exe http://127.0.0.1:8000/api/dashboard

The API returns structured dashboard data including:

Active blind spots
High-severity blind spots
Cases analyzed
Top blind spots
Yearly trends
Monthly prediction vs actual data

Example:

{
  "active_blind_spots": 124,
  "high_severity_count": 0,
  "cases_analyzed": 5320297
}
Frontend Dashboard

Once both servers are running:

Backend:
http://127.0.0.1:8000

Frontend:
http://localhost:3000

Open:

http://localhost:3000

The frontend communicates with the FastAPI backend to populate the CivicSage dashboard.

Demo Flow

The recommended demo flow is:

1. Start With the Dashboard

Show the overall operational picture.

Highlight:

Number of cases analyzed
Number of blind spots
High-risk areas
Historical trends
Prediction vs actual performance
2. Open Blind Spots

Show how CivicSage ranks departments and regions based on multiple operational signals.

Select a significant blind spot.

3. Explain the Risk Score

Show that the score is not based on a single metric.

Explain:

Backlog Risk       -> 35%
Aging Risk         -> 30%
Resolution Risk    -> 20%
Volume Score       -> 15%
4. Highlight Exasol

Explain that the heavy analytical computation is executed directly inside Exasol using SQL.

This is the key database component of the architecture.

5. Reality Check

Compare administrative performance against citizen-facing signals.

Look for contradictions such as:

Resolution Rate      Improving
Citizen Complaints   Increasing
Repeat Contacts      Increasing

This is where a conventional KPI dashboard may miss the problem.

6. AI Investigation

Open an identified blind spot and generate an investigation brief.

The AI layer helps summarize:

The observed anomaly
Supporting evidence
Potential causes
Recommended areas for human review
7. Evidence Chain

Show how the investigation can be traced back to the supporting signals.

8. Impact Tracker

Demonstrate how changes can be evaluated over time.

Key Insight

The main idea behind CivicSage is simple:

A high administrative resolution rate does not automatically mean a high-quality citizen outcome.

CivicSage therefore looks for contradictions between different layers of the system.

              OFFICIAL METRICS
                    |
                    v
             "Cases resolved"
                    |
                    |
                    v
              CIVICSAGE
                    |
       +------------+------------+
       |            |            |
       v            v            v
   Backlog       Aging       Resolution
       |            |            |
       +------------+------------+
                    |
                    v
              Citizen Signals
                    |
                    v
             Reality Check
                    |
                    v
             Blind Spot
                    |
                    v
            AI Investigation
                    |
                    v
                 Evidence
                    |
                    v
                 Action
                    |
                    v
                 Impact
Why CivicSage?

Most dashboards tell decision-makers:

"What happened?"

CivicSage tries to answer:

"Where might the numbers be hiding a problem?"

The platform combines:

Scale

Large-scale analytical processing through Exasol.

Detection

Multi-signal blind-spot identification.

Explanation

AI-assisted investigation.

Evidence

Traceable supporting signals.

Action

Human review and impact tracking.

This creates a complete intelligence pipeline:

DATA
  |
  v
SIGNAL
  |
  v
BLIND SPOT
  |
  v
INVESTIGATION
  |
  v
EVIDENCE
  |
  v
ACTION
  |
  v
IMPACT
Design Philosophy

CivicSage is designed around five principles:

1. Detect, Don't Just Display

The system should identify unusual or risky patterns instead of simply displaying charts.

2. Multi-Signal Analysis

A single KPI can be misleading.

CivicSage combines multiple signals before flagging a potential blind spot.

3. Explainable Intelligence

Every identified blind spot should have understandable indicators behind it.

4. Human-in-the-Loop

AI-generated findings are intended to assist investigators, not replace human judgment.

5. Evidence Before Action

Potential problems should be supported by observable data before decisions are made.

Performance Philosophy

CivicSage uses Exasol for analytical workloads because civic operational datasets can grow to millions of records.

Instead of performing all aggregation and scoring in the application layer:

Large Dataset
     |
     v
Python
     |
     v
Memory
     |
     v
Calculations

CivicSage pushes analytical computation into Exasol:

Large Dataset
     |
     v
EXASOL
     |
     +-- Aggregation
     +-- Normalization
     +-- Scoring
     +-- Ranking
     |
     v
Small Analytical Result
     |
     v
FastAPI

This keeps the application layer focused on serving insights rather than performing the entire analytical workload.

Data Quality and Prototype Disclaimer

CivicSage is an educational and hackathon prototype.

The datasets used in the demonstration are synthetic and/or prepared specifically for the prototype. They do not represent official government records, live government systems, real citizen complaints, or official public-service performance.

Risk scores are analytical indicators and should not be interpreted as definitive judgments about a department, region, organization, or public servant.

AI-generated investigation results are intended to assist human review and should always be validated against appropriate evidence.

Future Improvements

Potential future development includes:

Live civic data ingestion
More granular geographic analysis
Streaming operational data
Automated anomaly detection
Advanced citizen sentiment analysis
More sophisticated causal analysis
Predictive backlog forecasting
Automated intervention recommendations
Real-time Exasol analytics
Role-based investigator workflows
Audit trails for investigation decisions
Expanded AI evidence reasoning
Project Highlights
+--------------------------------------+
|            CIVICSAGE                 |
+--------------------------------------+
|                                      |
|  5.32M+ Cases Analyzed               |
|                                      |
|  124 Blind Spots Detected            |
|                                      |
|  Exasol-Powered Analytics             |
|                                      |
|  AI-Assisted Investigation            |
|                                      |
|  Reality Check Engine                 |
|                                      |
|  Evidence Chain                       |
|                                      |
|  Impact Tracking                      |
|                                      |
+--------------------------------------+
Repository Structure
CivicSage
|
+-- backend
|   |
|   +-- FastAPI application
|   +-- Exasol integration
|   +-- SQL analytics
|   +-- Blind-spot detection
|   +-- AI investigation
|   +-- Evidence services
|   +-- Data pipeline
|
+-- frontend
|   |
|   +-- Next.js application
|   +-- React components
|   +-- Dashboard
|   +-- Investigation UI
|   +-- Analytics visualizations
|
+-- README.md
Security

The project follows basic credential protection practices.

Sensitive values are stored locally in environment variables and are not intended to be committed to GitHub.

Before pushing changes, verify:

.env

is ignored by Git.

Only safe configuration templates such as:

.env.example

should be committed.

License

This project is currently intended for educational, research, hackathon, and prototype/demo purposes.

Exasol AI Build Challenge 2026

CivicSage was built to demonstrate how a high-performance analytical database can become the foundation of an AI-powered decision-support system.

The key idea is not simply:

"Store civic data in Exasol."

It is:

"Use Exasol to transform large-scale civic data into actionable intelligence."

CivicSage connects:

Large-Scale Data
       |
       v
     Exasol
       |
       v
Analytical Intelligence
       |
       v
Blind-Spot Detection
       |
       v
AI Investigation
       |
       v
Evidence
       |
       v
Human Decision
       |
       v
Impact Tracking
Built With

Exasol | AWS | FastAPI | Next.js | React | Python | SQL | AI

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

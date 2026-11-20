# Healthcare Billing Data Warehouse

## Overview

An end-to-end data engineering and analytics portfolio project built using synthetic healthcare billing data. This project demonstrates relational data modeling, Python-based data generation, PostgreSQL warehousing, data quality validation, Docker containerization, automated CI security scanning, CSV-based data ingestion, Databricks SQL analytics, and dashboard development.

**All data is synthetic. No real patient information is used.**

## Technology Stack

- Python
- PostgreSQL 18
- SQL
- Docker and Docker Compose
- GitHub Actions
- Trivy vulnerability scanner
- PowerShell
- Databricks SQL
- Unity Catalog
- Git and GitHub

## Project Workflow

1. Generate synthetic healthcare billing data using Python.
2. Load and organize data in PostgreSQL.
3. Structure data into raw, staging, warehouse, and reporting schemas.
4. Validate relationships, billing amounts, and data consistency.
5. Containerize the Python application and PostgreSQL service using Docker Compose.
6. Validate application-to-database connectivity.
7. Export nine warehouse tables to CSV.
8. Upload CSV files to a Databricks Unity Catalog volume.
9. Create Databricks tables and reconcile source and destination row counts.
10. Develop reporting views for collections, denials, payer performance, and claim-level financial analysis.
11. Build and publish a Healthcare Billing Analytics Dashboard.
12. Run automated Docker build, database connectivity, and vulnerability checks through GitHub Actions.

## Project Documentation

- [Architecture Diagram](docs/architecture.md) — visual overview of the pipeline from Python through PostgreSQL and Databricks to the analytics dashboard.
- [Project Walkthrough](docs/project-walkthrough.md) — step-by-step explanation of the implementation, dataset, SQL reporting views, and validation results.
- [Data Model Diagram (ERD)](docs/data-model.md) — shows the relationships between patients, encounters, claims, payers, payments, denials, and adjustments.

## Data Model

The project contains nine warehouse entities:

| Entity | Description |
|---|---|
| Patient | Synthetic patient demographic and identification data |
| Provider | Healthcare provider reference information |
| Payer | Insurance payer reference information |
| Encounter | Patient encounter and service information |
| Claim | Billing claim header information |
| Claim Line | Individual billed services and charge details |
| Payment | Payment transactions associated with claims |
| Denial | Claim denial information |
| Adjustment | Financial adjustments associated with billing records |

### Databricks Dataset Volume

| Entity | Records |
|---|---:|
| Patient | 10,000 |
| Provider | 5 |
| Payer | 5 |
| Encounter | 18,107 |
| Claim | 17,250 |
| Claim Line | 34,438 |
| Payment | 8,575 |
| Denial | 2,046 |
| Adjustment | 3,460 |
| **Total** | **93,886** |

**Total records across the nine entities:** 93,886.

*These figures describe the documented Databricks dataset. The smaller Docker generator validation run is documented separately under Docker Validation.*

## PostgreSQL Reporting Views

The PostgreSQL reporting layer contains:

- `reporting.claim_ar`
- `reporting.denial_summary`
- `reporting.monthly_collections`
- `reporting.payer_performance`

These views support healthcare billing analysis, including accounts receivable, denial trends, monthly collections, and payer performance.

## Docker Containerization

The application and PostgreSQL database are configured using Docker and Docker Compose.

### Docker Architecture

The containerized application consists of two services:

| Service | Purpose |
|---|---|
| `postgres` | Runs PostgreSQL 18 and stores healthcare billing data. |
| `app` | Runs the Python application and connects to PostgreSQL. |

The application connects to PostgreSQL through the Docker Compose service network using the hostname `postgres`.

The PostgreSQL service uses a persistent named Docker volume:

`healthcare_billing_data`

This allows database data to persist when containers are stopped and restarted.

### Docker Security Controls

The Docker implementation includes:

- Python slim base image.
- Debian package updates during image construction.
- Application execution under a dedicated non-root user (`appuser`, UID 10001).
- Environment-based database credentials instead of hardcoded passwords.
- `.env` excluded from Git using `.gitignore`.
- `.dockerignore` prevents secrets, Git metadata, virtual environments, and temporary files from entering the Docker build context.
- PostgreSQL port binding restricted to `127.0.0.1:5432`.
- Pip removed from the final application image to reduce unnecessary packaged tooling.

### Docker Setup

Prerequisites:

- Docker Engine
- Docker Compose
- Git

Configure the environment variables required by Docker Compose in a local `.env` file. Keep actual database credentials private and never commit this file.

Build the application image:

```bash
docker compose build app
```

Start PostgreSQL:

```bash
docker compose up -d postgres
```

Check PostgreSQL readiness:

```bash
docker compose exec -T postgres pg_isready -U postgres -d healthcare_billing
```

Run a database connectivity check from the application container:

```bash
docker compose run --rm --no-deps app python -c '
import os
import psycopg

with psycopg.connect(
    host=os.environ["PGHOST"],
    port=os.environ["PGPORT"],
    dbname=os.environ["PGDATABASE"],
    user=os.environ["PGUSER"],
    password=os.environ["PGPASSWORD"],
) as conn:
    print("Database:", conn.execute(
        "SELECT current_database()"
    ).fetchone()[0])
    print("Docker application connectivity: SUCCESS")
'
```

Stop the services without deleting the persistent database volume:

```bash
docker compose down
```

**Important:** The default application container command runs the synthetic data generator. Do not run it against an already populated database unless the generator's loading and duplicate-protection behavior has been reviewed.

## Docker Validation

The Docker implementation was tested in GitHub Codespaces.

### Verified Results

| Validation | Result |
|---|---|
| Docker Compose configuration | Passed |
| Docker application image build | Passed |
| PostgreSQL container startup | Passed |
| PostgreSQL readiness check | Passed |
| Python application connectivity | Passed |
| Database selected | `healthcare_billing` |
| Existing database data | Preserved during connectivity testing |

The successful application connectivity test returned:

```text
Database: healthcare_billing
Docker application connectivity: SUCCESS
```

### Docker Synthetic Data Generation Test

The earlier Docker synthetic data generation test loaded:

| Entity | Records |
|---|---:|
| Patients | 1,000 |
| Encounters | 1,804 |
| Claims | 1,713 |
| Claim Lines | 3,451 |
| Payments | 811 |
| Denials | 216 |
| Adjustments | 293 |
| **Generated records subtotal** | **9,288** |
| Providers (reference data) | 5 |
| Payers (reference data) | 5 |
| **Total across nine entities** | **9,298** |

The 9,288 generated records cover seven entities. The additional 10 records are reference data consisting of five providers and five payers.

These counts represent the Docker generator test and are separate from the larger Databricks dataset documented in the Data Model section.

## GitHub Actions CI/CD

A dedicated Docker CI workflow is configured in:

`.github/workflows/docker-ci.yml`

The workflow runs automatically for:

- Pushes to `main`
- Pull requests targeting `main`
- Manual workflow dispatch

### CI Pipeline Steps

1. Check out the repository.
2. Create a temporary CI environment file with disposable test credentials.
3. Validate the Docker Compose configuration.
4. Build the Docker application image.
5. Start PostgreSQL.
6. Wait for PostgreSQL readiness.
7. Verify Python application connectivity to PostgreSQL.
8. Scan the Docker image using Trivy.
9. Apply a separate CRITICAL vulnerability gate.
10. Stop PostgreSQL and clean up the CI containers.

### GitHub Actions Security Controls

- Repository permissions are restricted to read-only contents access.
- Checkout credentials are not persisted.
- CI database credentials are temporary and used only for testing.
- Trivy scans the built Docker image.
- The first scan reports HIGH and CRITICAL findings without failing solely on HIGH findings.
- A separate CRITICAL-only scan fails the workflow if CRITICAL vulnerabilities are detected.
- The PostgreSQL cleanup step runs even when earlier steps fail.

### Verified CI Execution

| Detail | Value |
|---|---|
| Workflow | Docker CI |
| Run | #1 |
| Commit | `aadaf09` |
| Branch | `main` |
| Job | Build, Validate and Scan Docker Image |
| Total duration | 55 seconds |
| Job duration | 51 seconds |
| Result | Success |

All Docker CI job steps completed successfully, including image build, database connectivity, both Trivy scans, and PostgreSQL cleanup.

The existing Actionlint, Python Quality Checks, Gitleaks, and Trivy filesystem security workflows also passed for the same commit.

## Docker Image Vulnerability Scanning

Trivy is used to scan the built Docker application image for vulnerabilities.

### GitHub Actions Scan Result

The Docker CI run on November 20, 2026, reported:

| Scanned target | Reported vulnerabilities |
|---|---:|
| Debian 13.7 | 0 |
| psycopg 3.3.6 package metadata | 0 |
| psycopg-binary 3.3.6 package metadata | 0 |
| **Total reported** | **0** |

The CRITICAL-only security gate also completed successfully.

### Local and GitHub Scan Result Difference

An earlier local Docker image scan reported:

| Scan environment | Trivy version | Debian HIGH | CRITICAL |
|---|---|---:|---:|
| Local Codespaces scan | 0.76.0 | 46 | 0 |
| GitHub Actions scan | Not recorded | 0 reported | 0 reported |

The GitHub Actions report showed zero findings for its listed Debian and Python package targets.

**Investigation note:** These results are different and should not be interpreted as proof that all previously identified vulnerabilities were fixed. The scans may have used different Trivy versions, vulnerability database states, or image contents. The image digest, build contents, scanner versions, and vulnerability database versions must be compared before drawing a remediation conclusion.

The GitHub Actions scan result is the verified result for CI run #1, not a guarantee that future image builds will remain vulnerability-free.

## Databricks Implementation

**Catalog:** `workspace`

The Databricks implementation provides the analytics layer of the project.

The workflow includes:

- Uploading CSV files to a Databricks Unity Catalog volume.
- Creating Databricks tables from the exported PostgreSQL warehouse data.
- Reconciling source and destination row counts.
- Developing SQL reporting views for healthcare billing analytics.
- Building and publishing a Healthcare Billing Analytics Dashboard.

The documented Databricks dataset contains 93,886 records across nine warehouse entities.

## Data Quality and Validation

Data quality checks are included to validate the generated healthcare billing dataset and the warehouse structure.

Validation covers:

- Database connectivity.
- Table existence and row counts.
- Relationships between warehouse entities.
- Billing amounts and financial consistency.
- Source and destination row-count reconciliation.
- Reporting query validation.

The project includes Python scripts for database connection testing, table checks, row-count checks, and load-state validation.

## Repository Contents

- `scripts/` — Python data generation, connection, and validation scripts.
- `sql/` — SQL reporting view definitions.
- `database/` — PostgreSQL schema and reference data initialization scripts.
- `docs/` — Architecture, data model, and project walkthrough documentation.
- `.github/workflows/` — GitHub Actions CI and security workflows.
- `Dockerfile` — Python application image definition.
- `compose.yaml` — PostgreSQL and application service configuration.
- `.dockerignore` — Excludes unnecessary and sensitive files from Docker build context.
- `.gitignore` — Excludes local data, backups, virtual environments, and generated files.
- `README.md` — Project documentation.

## Future Enhancements

- Develop automated incremental ingestion.
- Expand data quality monitoring and reporting.
- Document the SQL definitions for all reporting views in the repository.
- Investigate and reconcile differences between local and GitHub Trivy scan results.
- Add image publishing to a container registry when registry credentials and deployment requirements are configured.

## Data Privacy

This project uses synthetic healthcare billing data for learning, development, and portfolio demonstration purposes.

No real patient information, protected health information (PHI), or production healthcare billing records are included.

Database credentials are maintained in local environment configuration and are excluded from Git version control.

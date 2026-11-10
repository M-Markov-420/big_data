# Project Migration Analysis Pipeline

## Overview and Purpose
The Project Migration Analysis Pipeline is a data processing tool designed to evaluate the readiness of software projects (primarily .NET codebases) for migration or upgrading. It processes raw analytical data from a CSV file containing code analysis findings, categorizes these findings, calculates risk scores for individual projects, and generates actionable CSV reports. 

The primary goals of this tool are to:
1. **Identify Migration Blockers:** Highlight mandatory framework upgrades, deprecated APIs, and required NuGet package updates.
2. **Quantify Risk:** Assign a standardized `RiskScore` and `RiskClass` to each project based on the severity and frequency of findings.
3. **Pinpoint Hotspots:** Identify which specific technologies (e.g., EF Core, ASP.NET Core) or packages are causing the most issues.
4. **Provide Actionable Output:** Generate specific reports that development teams can use to plan their migration sprints (e.g., project issue matrices, package upgrade lists).

---

## Architecture
To maintain readability and scalability, the application is divided into specific modules based on the Separation of Concerns principle. 

### 1. `config.py`
**Purpose:** Centralizes all configurable variables and hardcoded constants.
*   **Key Contents:** Path to the input dataset (`CSV_FILE`), lists of issue IDs to process (`ISSUES_TO_KEEP`), and issue IDs to explicitly ignore (`ISSUE_TO_IGNORE`). 
*   **Why it exists:** If the target dataset changes or new issue types need to be tracked, developers only need to update this file without altering the core logic.

### 2. `preprocessing.py`
**Purpose:** Handles data ingestion and initial sanitization.
*   **Key Functions:** `load_and_filter_data()`
*   **How it works:** Loads the CSV file into a Pandas DataFrame and applies early filters. It removes package internals (Binary locations) and drops findings that are irrelevant to the migration based on the configuration rules.

### 3. `features.py`
**Purpose:** Contains the domain-specific logic for feature engineering (creating new data points from existing raw text).
*   **Key Functions:** 
    *   `_get_project_name()`: Cleans up raw file paths to extract clean project names (e.g., stripping `.csproj`).
    *   `_detect_technology()`: Scans incident descriptions for keywords to categorize the technology involved (e.g., mapping "EntityFrameworkCore" to "EF Core").
    *   `_get_category()`: Classifies the project into domains like "Gateway", "Services", or "Tests" based on its directory path.
    *   `apply_features()`: Applies these transformations to the DataFrame.

### 4. `analysis.py`
**Purpose:** Houses the mathematical and aggregation logic of the pipeline.
*   **Key Functions:** `build_project_summary()`
*   **How it works:** This is the analytical engine. It groups the cleaned data by project and tallies severities (Mandatory, Optional, etc.), required NuGet recommendations, deprecated API findings, and unique incident counts. It joins these metrics into a single `summary` DataFrame.
*   **Risk Scoring:** Calculates a custom risk formula: 
    `(Mandatory * 20) + (NuGet * 10) + (Unique Incidents * 5) + (Framework Upgrades * 20)`
    It then classifies this score into risk tiers (Critical, High, Medium, Low).

### 5. `output_manager.py`
**Purpose:** Manages all external side effects, strictly separating the calculation of data from the presentation of data.
*   **Key Functions:** 
    *   `export_csv_reports()`: Slices the processed DataFrames into targeted views and saves them to disk (e.g., `project_issue_matrix.csv`, `technology_hotspots.csv`, `mandatory_api_findings.csv`).
    *   `print_console_summary()`: Generates terminal-friendly, human-readable summaries of top packages, issue types, and high-risk projects.

### 6. `main.py`
**Purpose:** The orchestrator script.
*   **How it works:** It acts as the entry point for the application. It sequentially imports and calls the functions from the other modules, explicitly defining the flow of data: *Ingest -> Feature Engineer -> Analyze -> Export*.

---

## How to Run
Ensure you have Python installed along with the `pandas` library. Place your target CSV file (configured in `config.py`) in the root directory, and execute the orchestrator:

```bash
pip install pandas
python main.py
```
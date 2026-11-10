# Project Migration Analysis Pipeline

## Overview

The **Project Migration Analysis Pipeline** is a modular Python-based data processing tool designed to evaluate the readiness of software projects (primarily .NET codebases) for migration or upgrading. 

It ingests raw code analysis findings, sanitizes the data, calculates customizable risk scores, and exports granular reports. These reports help development teams identify migration blockers, isolate deprecated APIs, and plan their migration sprints efficiently.

---

## 📂 Project Structure

The project is organized to separate code, configuration, input data, and generated artifacts cleanly. 

```mermaid
classDiagram
    class big_data {
    }
    
    class Code {
        +analysis.py
        +config.py
        +features.py
        +main.py
        +output_manager.py
        +preprocessing.py
    }
    
    class Documentation {
        +project_structure.md
        +README.md
    }
    
    class Input {
        +finalr.csv
    }
    
    class Output {
        +api_deprecations.csv
        +mandatory_api_findings.csv
        +package_upgrades.csv
        +project_issue_matrix.csv
        +project_summary.csv
        +technology_hotspots.csv
        +unique_findings.csv
    }
    
    class Project_Details {
        +ProjectName_details.csv
        +... (Individual project reports)
    }

    %% Composition Relationships
    big_data *-- Code : contains
    big_data *-- Documentation : contains
    big_data *-- Input : contains
    big_data *-- Output : contains
    Output *-- Project_Details : contains
```

---

## 🧩 Architecture & Modules

The codebase follows the **Separation of Concerns** principle, dividing the data pipeline into single-responsibility modules:

*   **`config.py`**: The universal state. Resolves directory paths dynamically and stores business rules (e.g., target Issue IDs, file paths).
*   **`preprocessing.py`**: Handles data ingestion. Cleans the raw CSV by removing internal binary files and filtering out irrelevant issues.
*   **`features.py`**: The domain logic engine. Parses strings to engineer new columns like "Project", "Technology", and "Category".
*   **`analysis.py`**: The math engine. Groups data, pivots severity counters, calculates unique incidents, and applies the custom `RiskScore` formula.
*   **`output_manager.py`**: Manages side effects. Writes the aggregated dataframes to CSVs in the `Output` folders and prints a terminal summary.
*   **`main.py`**: The orchestrator. Imports the above modules and executes the pipeline in a readable, sequential flow.

### Module Dependencies

```mermaid
flowchart TD
    subgraph Pipeline Architecture
        M[main.py]
        P[preprocessing.py]
        F[features.py]
        A[analysis.py]
        O[output_manager.py]
        C[config.py]
    end

    M -->|Imports & Orchestrates| P
    M -->|Imports & Orchestrates| F
    M -->|Imports & Orchestrates| A
    M -->|Imports & Orchestrates| O

    P -->|Reads Settings| C
    O -->|Reads Export Paths| C
    
    classDef orchestrator fill:#f9f,stroke:#333,stroke-width:2px;
    classDef worker fill:#bbf,stroke:#333,stroke-width:1px;
    classDef state fill:#dfd,stroke:#333,stroke-width:1px;
    
    class M orchestrator;
    class P,F,A,O worker;
    class C state;
```

---

## 🔄 Data Flow & Execution

The pipeline transforms a raw CSV dump into structured intelligence through a strict top-to-bottom sequence.

### 1. High-Level Activity Flow

```mermaid
flowchart TD
    Raw[(Input: finalr.csv)] --> Preprocess{preprocessing.py}
    
    Preprocess -->|Drop 'Binary' locations| F1[Filtered Data]
    Preprocess -->|Remove 'Api.0002'| F1
    Preprocess -->|Keep Target IDs| F1
    
    F1 --> Features{features.py}
    Features -->|Parse Project Names| E1[Enriched Data]
    Features -->|Map Incident to Technology| E1
    Features -->|Categorize by Path| E1
    
    E1 --> Analysis{analysis.py}
    Analysis -->|Group Severity Counters| S1[Aggregated Summary]
    Analysis -->|Sum Story Points| S1
    Analysis -->|Calculate Unique Incidents| S1
    
    S1 --> RiskCalc[Apply Risk Formula]
    RiskCalc --> S2[Final Scored Summary]
    
    E1 --> Output{output_manager.py}
    S2 --> Output
    
    Output -->|Write| Disk1[(Standard CSV Reports)]
    Output -->|Split & Write| Disk2[(Project_Details CSVs)]
    Output -->|Print| Console[Terminal Output]
```

### 2. Execution Sequence

```mermaid
sequenceDiagram
    participant M as main.py
    participant C as config.py
    participant P as preprocessing.py
    participant F as features.py
    participant A as analysis.py
    participant O as output_manager.py

    M->>P: load_and_filter_data()
    P->>C: Fetch CSV_FILE, target IDs
    P-->>M: Returns filtered DataFrame (df)
    
    M->>F: apply_features(df)
    Note right of F: Engineers Project, Technology, & Category
    F-->>M: Returns enriched DataFrame (df)
    
    M->>A: build_project_summary(df)
    Note right of A: Groups data & computes RiskScore
    A-->>M: Returns summary DataFrame (summary)
    
    M->>O: export_csv_reports(df, summary)
    O->>C: Fetch OUTPUT_DIR
    Note right of O: Writes matrix, hotpots, API, and NuGet CSVs
    O-->>M: (Generates general CSVs)
    
    M->>O: export_project_details(df)
    O->>C: Fetch PROJECTS_DIR
    Note right of O: Generates a distinct CSV for each project
    O-->>M: (Generates project-specific CSVs)
    
    M->>O: print_console_summary(df, summary)
    O-->>M: (Prints summary to Terminal)
```

---

## 🚀 Getting Started

### Prerequisites
* Python 3.8+
* `pandas` library

Install dependencies using pip:
```bash
pip install pandas
```

### Execution
Ensure your input file (`finalr.csv`) is placed in the `Input` directory, then run the orchestrator script:

```bash
cd Code
python main.py
```

### Outputs
Upon successful execution, the terminal will display a high-level summary. The detailed findings will be generated in the automatically created `Output` folder:
* **`project_summary.csv`**: Master list of all projects and their risk scores.
* **`technology_hotspots.csv`**: Frequencies of specific framework/library issues.
* **`package_upgrades.csv`**: Detailed list of required NuGet updates.
* **`Project_Details/`**: A subdirectory containing isolated, severity-sorted `.csv` files for *every individual project*.
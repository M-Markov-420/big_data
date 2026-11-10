sequenceDiagram
    participant M as main.py
    participant C as config.py
    participant P as preprocessing.py
    participant F as features.py
    participant A as analysis.py
    participant O as output_manager.py

    M->>P: load_and_filter_data()
    P->>C: Fetch CSV_FILE, ISSUES_TO_KEEP, ISSUE_TO_IGNORE
    P-->>M: Returns filtered DataFrame (df)
    
    M->>F: apply_features(df)
    Note right of F: Engineers 'Project', 'Technology', & 'Category' columns
    F-->>M: Returns enriched DataFrame (df)
    
    M->>A: build_project_summary(df)
    Note right of A: Groups data, joins counts, & computes RiskScore
    A-->>M: Returns summary DataFrame (summary)
    
    M->>O: export_csv_reports(df, summary)
    O->>C: Fetch OUTPUT_DIR
    Note right of O: Writes matrix, hotpots, API, and NuGet CSVs
    O-->>M: (Side effect: General files saved to disk)
    
    M->>O: export_project_details(df)
    O->>C: Fetch PROJECTS_DIR
    Note right of O: Loops through projects & sorts by Schweregrad
    O-->>M: (Side effect: Individual project CSVs saved to disk)
    
    M->>O: print_console_summary(df, summary)
    Note right of O: Outputs Top Packages, Issues, and Risk rankings
    O-->>M: (Side effect: Terminal output generated)
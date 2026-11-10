classDiagram
    
    class Code {
        +analysis.py
        +config.py
        +features.py
        +main.py
        +output_manager.py
        +preprocessing.py
    }
    
    class __pycache__ {
        +analysis.cpython-315.pyc
        +config.cpython-315.pyc
        +features.cpython-315.pyc
        +output_manager.cpython-315.pyc
        +preprocessing.cpython-315.pyc
    }
    
    class Documentation {
        +10112026.md
        +Code.md
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
        +Leuze.RES.Analyzers.Tests_details.csv
        +Leuze.RES.Common.Authentication_details.csv
        +Leuze.RES.Common.SystemServiceReadinessClient_details.csv
        +... (and 33 other project detail CSVs)
    }

    %% Composition Relationships (Folders containing subfolders)
    big_data *-- Code : contains
    big_data *-- Documentation : contains
    big_data *-- Input : contains
    big_data *-- Output : contains
    Code *-- __pycache__ : contains
    Output *-- Project_Details : contains
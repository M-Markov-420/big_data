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
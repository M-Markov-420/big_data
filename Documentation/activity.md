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
import pandas as pd
from config import CSV_FILE, ISSUES_TO_KEEP, ISSUE_TO_IGNORE

def load_and_filter_data():
    df = pd.read_csv(
        CSV_FILE,
        encoding="utf-8",
        sep=",",
        engine="python"
    )

    # Ignore package internals
    df = df[~df["Art des Speicherorts"].eq("Binary")]

    # Ignore specific API issue
    df = df[df["Issue-ID"] != ISSUE_TO_IGNORE]

    # Keep only migration-relevant findings
    df = df[df["Issue-ID"].isin(ISSUES_TO_KEEP)]
    
    return df
import pandas as pd
from pathlib import Path

def _get_project_name(path):
    if pd.isna(path):
        return "Unknown"
    filename = Path(path).name
    if filename.endswith(".csproj"):
        return filename.replace(".csproj", "")
    return filename

def _detect_technology(incident):
    if pd.isna(incident): return "Unknown"
    if "EntityFrameworkCore" in incident: return "EF Core"
    if "AspNetCore" in incident: return "ASP.NET Core"
    if "Newtonsoft.Json" in incident: return "Newtonsoft.Json"
    if "CodeAnalysis" in incident: return "Roslyn"
    if "RabbitMQ" in incident: return "RabbitMQ"
    if "Grpc" in incident: return "gRPC"
    if "Opc" in incident: return "OPC UA"
    return "Other"

def _get_category(path):
    if not isinstance(path, str): return "Other"
    if "Common" in path: return "Common"
    if "Gateways" in path: return "Gateway"
    if "Services" in path: return "Services"
    if "Tests" in path: return "Tests"
    if "Analyzers" in path: return "Analyzers"
    return "Other"

def apply_features(df):
    df["Project"] = df["Projektpfad"].apply(_get_project_name)
    df["Technology"] = df["Incident-ID"].apply(_detect_technology)
    df["Category"] = df["Projektpfad"].apply(_get_category)
    return df
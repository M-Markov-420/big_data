from config import OUTPUT_DIR, PROJECTS_DIR

def export_project_details(df):
    """Generates a detailed breakdown file for each individual project."""
    for project, group in df.groupby("Project"):
        # Ensure the project name is safe for Windows file paths
        safe_name = "".join(c for c in str(project) if c.isalnum() or c in "._-").rstrip()
        file_path = PROJECTS_DIR / f"{safe_name}_details.csv"
        
        # Define the most relevant columns for a detailed project view
        desired_columns = [
            "Issue-ID", "Incident-ID", "Schweregrad", "Technology", 
            "Beschreibung", "Ausschnitt", "Hilfelink"
        ]
        
        # Keep only the columns that actually exist in the dataframe
        export_cols = [c for c in desired_columns if c in group.columns]
        
        # Sort so 'Mandatory' and higher severity items appear at the top
        sorted_group = group.sort_values(by=["Schweregrad", "Issue-ID"])
        
        # Export to the Project_Details subfolder
        sorted_group[export_cols].to_csv(file_path, index=False)


def export_csv_reports(df, summary):
    # Project & Matrix Exports
    summary.reset_index().to_csv(OUTPUT_DIR / "project_summary.csv", index=False)
    
    df.groupby(["Project", "Issue-ID"]).size().unstack(fill_value=0).to_csv(OUTPUT_DIR / "project_issue_matrix.csv")

    # NuGet Exports
    nuget_df = df[df["Issue-ID"] == "NuGet.0002"]
    nuget_df[["Project", "Beschreibung", "Ausschnitt"]].to_csv(OUTPUT_DIR / "package_upgrades.csv", index=False)

    # API Exports
    api_df = df[df["Issue-ID"] == "Api.0003"]
    api_df[["Project", "Incident-ID", "Assemblyname", "Assemblyversion", "Hilfelink"]].to_csv(OUTPUT_DIR / "api_deprecations.csv", index=False)
    api_df[api_df["Schweregrad"] == "Mandatory"].to_csv(OUTPUT_DIR / "mandatory_api_findings.csv", index=False)

    # Findings & Technology Exports
    df[["Issue-ID", "Incident-ID", "Beschreibung"]].drop_duplicates().to_csv(OUTPUT_DIR / "unique_findings.csv", index=False)
    df.groupby("Technology").size().sort_values(ascending=False).to_csv(OUTPUT_DIR / "technology_hotspots.csv")


def print_console_summary(df, summary):
    # (Keep your existing print_console_summary function exactly as it is)
    print("\n--- Top Issue Types ---")
    print(df.groupby("Issue-ID").size().sort_values(ascending=False).head(20))

    print("\n--- Top Packages ---")
    nuget_df = df[df["Issue-ID"] == "NuGet.0002"]
    print(nuget_df.groupby("Ausschnitt").size().sort_values(ascending=False).head(50))

    print("\n--- Project Category Summary ---")
    print(df.groupby("Category").size().sort_values(ascending=False))

    print("\n--- Mandatory Findings Only ---")
    mandatory = df[df["Schweregrad"] == "Mandatory"]
    print(mandatory.groupby("Project").size().sort_values(ascending=False))

    print("\n" + "=" * 80)
    print("PROJECT MIGRATION SUMMARY")
    print("=" * 80)
    
    display_cols = ["TotalFindings", "Mandatory", "Optional", "Potential", "RiskScore", "RiskClass"]
    print(summary[display_cols].sort_values("RiskScore", ascending=False))

    print(f"\nProjects analyzed: {summary.shape[0]}")
    print(f"Total findings: {summary['TotalFindings'].sum()}")
    print(f"Total story points: {summary['StoryPoints'].sum()}")
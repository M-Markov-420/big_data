def _classify_risk(score):
    if score > 1000: return "Critical"
    if score > 300: return "High"
    if score > 100: return "Medium"
    return "Low"

def build_project_summary(df):
    # Severity Counters
    severity_counts = df.groupby(["Project", "Schweregrad"]).size().unstack(fill_value=0)
    for col in ["Mandatory", "Optional", "Potential", "Information"]:
        if col not in severity_counts:
            severity_counts[col] = 0

    # Aggregations
    story_points = df.groupby("Project")["Story Points"].sum().rename("StoryPoints")
    nuget_counts = df[df["Issue-ID"] == "NuGet.0002"].groupby("Project").size().rename("NuGetRecommendations")
    api_counts = df[df["Issue-ID"] == "Api.0003"].groupby("Project").size().rename("DeprecatedApiFindings")
    framework_counts = df[df["Issue-ID"] == "Project.0002"].groupby("Project").size().rename("FrameworkUpgradeRequired")
    unique_incidents = df.groupby("Project")["Incident-ID"].nunique().rename("UniqueIncidents")

    # Combine
    summary = severity_counts.join(story_points).join(nuget_counts).join(api_counts).join(framework_counts).join(unique_incidents)
    summary = summary.fillna(0)

    # Scoring
    summary["TotalFindings"] = summary["Mandatory"] + summary["Optional"] + summary["Potential"] + summary["Information"]
    summary["RiskScore"] = (
        summary["Mandatory"] * 20 +
        summary["NuGetRecommendations"] * 10 +
        summary["UniqueIncidents"] * 5 +
        summary["FrameworkUpgradeRequired"] * 20
    )
    summary["RiskClass"] = summary["RiskScore"].apply(_classify_risk)

    return summary
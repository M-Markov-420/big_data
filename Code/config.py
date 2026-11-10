from pathlib import Path

# Dynamically resolve the 'big_data' root folder
ROOT_DIR = Path(__file__).resolve().parent.parent

# Define folder paths
INPUT_DIR = ROOT_DIR / "Input"
OUTPUT_DIR = ROOT_DIR / "Output"
PROJECTS_DIR = OUTPUT_DIR / "Project_Details"

# Create the Output directories if they don't exist yet
OUTPUT_DIR.mkdir(exist_ok=True)
PROJECTS_DIR.mkdir(exist_ok=True)

# Point to the renamed input file
CSV_FILE = INPUT_DIR / "finalr.csv"

ISSUES_TO_KEEP = [
    "Project.0002",
    "NuGet.0002",
    "NuGet.0004",
    "NuGet.0005",
    "Api.0003"
]

ISSUE_TO_IGNORE = "Api.0002"
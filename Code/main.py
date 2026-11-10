from preprocessing import load_and_filter_data
from features import apply_features
from analysis import build_project_summary
from output_manager import export_csv_reports, print_console_summary, export_project_details

def main():
    # 1. Ingest & Filter
    df = load_and_filter_data()

    # 2. Engineer Features
    df = apply_features(df)

    # 3. Analyze & Group
    summary = build_project_summary(df)

    # 4. Generate Outputs
    export_csv_reports(df, summary)
    export_project_details(df)
    print_console_summary(df, summary)

if __name__ == "__main__":
    main()
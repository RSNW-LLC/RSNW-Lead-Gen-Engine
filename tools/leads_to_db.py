import dlt
import pandas as pd
import os

def load_leads_to_duckdb():
    print("[*] Initializing dlt pipeline for Lead Intelligence...")
    
    csv_file = "data_outputs/master_lead_list.csv"
    if not os.path.exists(csv_file):
        print(f"[X] Error: {csv_file} not found. Run consolidation first.")
        return

    # Create a dlt pipeline
    pipeline = dlt.pipeline(
        pipeline_name='lead_intelligence_pipeline',
        pipelines_dir='intelligence_db',
        destination='duckdb',
        dataset_name='leads_data',
    )

    # Load the CSV data using pandas
    print(f"[*] Reading {csv_file}...")
    df = pd.read_csv(csv_file)
    
    # Clean up column names for DuckDB (lowercase, no spaces)
    df.columns = [c.lower().replace(' ', '_') for c in df.columns]

    # Run the pipeline
    print("[*] Loading data into DuckDB...")
    load_info = pipeline.run(df, table_name="all_leads", write_disposition="replace")
    
    print(load_info)
    print(f"\n[✓] Lead Intelligence Database Updated.")
    print(f"[*] Database file: {pipeline.pipeline_name}.duckdb")
    print("[*] To explore the data, run: uv run dlthub show")

if __name__ == "__main__":
    load_leads_to_duckdb()

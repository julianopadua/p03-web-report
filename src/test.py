import os
import pandas as pd

# Define the directory where the CSV files are stored
data_dir = os.path.join(os.path.dirname(__file__),"..","data", "processed")

# Ensure the directory exists
if not os.path.exists(data_dir):
    print("Error: The directory 'data_processed' does not exist.")
    exit()

# List all CSV files with '_analysis.csv' in the name
csv_files = [f for f in os.listdir(data_dir) if f.endswith("_analysis.csv")]

if not csv_files:
    print("No analysis CSV files found.")
    exit()

# Iterate through each CSV file
for csv_file in csv_files:
    csv_path = os.path.join(data_dir, csv_file)

    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_path)

    # Print file name
    print(f"\n--- Data from {csv_file} ---\n")

    # Extract and print the Description
    if "Description" in df.columns:
        print("📌 Description:")
        print(df["Description"].iloc[0])  # Print first row of Description
        print("\n" + "-"*50 + "\n")  

    # Extract and print the Plot Path
    if "Plot Path" in df.columns:
        print("📂 Plot Path:")
        print(df["Plot Path"].iloc[0])  # Print first row of Plot Path
        print("\n" + "-"*50 + "\n")  

    # Print Market Cap separately if it exists
    if "Market Cap" in df.columns:
        print("💰 Market Cap:")
        print(df["Market Cap"].iloc[0])
        print("\n" + "-"*50 + "\n")

    # Print all other financial ratios
    print("📊 Financial Ratios:")
    for col in df.columns:
        if col not in ["Description", "Plot Path", "Market Cap"]:  # Skip already printed fields
            print(f"{col}: {df[col].iloc[0]}")

    print("\n" + "="*50 + "\n")  # Separator for readability

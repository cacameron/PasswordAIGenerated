import pandas as pd
import csv
from pathlib import Path


# Project directory
BASE_DIR = Path(__file__).resolve().parent

# Dataset directory
DATASET_DIR = BASE_DIR / "Dataset"


# 1. LOAD THE DATA
def load_dataset(file_path):

    # Count incorrectly formatted rows
    incorrect_rows = 0

    with open(file_path, "r", encoding="utf-8-sig", newline="") as file:

        reader = csv.reader(file)
        header = next(reader)

        for row in reader:

            if len(row) != len(header):
                incorrect_rows += 1

    # Load dataset and skip malformed rows
    data = pd.read_csv(
        file_path,
        engine="python",
        on_bad_lines="skip"
    )

    print("\nDataset loaded successfully!")
    print("Number of rows:", len(data))
    print("Number of columns:", len(data.columns))
    print("Incorrectly formatted rows excluded:", incorrect_rows)

    return data


# 2. INSPECT THE DATA
def inspect_dataset(data, dataset_name):

    print(f"\n--- Inspecting {dataset_name} ---")

    print("\nColumn Names:")
    print(data.columns.tolist())

    print("\nData Types:")
    print(data.dtypes)

    print("\nMissing Values:")
    print(data.isnull().sum())

    print("\nFirst 5 Rows:")
    print(data.head())


# 3. CLEAN THE DATA
def clean_dataset(data):

    # Create a copy of the original dataset
    data = data.copy()

    # Remove unnecessary spaces from column names
    data.columns = data.columns.str.strip()

    # Remove rows with missing values
    original_rows = len(data)

    data = data.dropna()

    removed_rows = original_rows - len(data)

    print("Rows with missing values removed:", removed_rows)

    # Remove unnecessary spaces from text columns
    for column in data.select_dtypes(include=["object"]).columns:
        data[column] = data[column].str.strip()

    print("\nData cleaned successfully!")
    return data


# 4. REMOVE DUPLICATES
def remove_duplicates(data):

    original_rows = len(data)

    data = data.drop_duplicates()

    removed_rows = original_rows - len(data)

    print("\nDuplicate Removal:")
    print("Duplicates removed:", removed_rows)
    print("Remaining rows:", len(data))

    return data


# 5. PREPARE THE DATASET
def prepare_dataset(data):

    # Reset index after cleaning
    data = data.reset_index(drop=True)

    print("\nDataset prepared successfully!")
    print("Final number of rows:", len(data))
    print("Final number of columns:", len(data.columns))

    return data


# MAIN PROGRAM
if __name__ == "__main__":

    datasets = {

        "Common Passwords":
            DATASET_DIR / "10,000 most common passwords.csv",

        "Password Strength Classifier":
            DATASET_DIR / "Password Strength Classifier.csv"

    }

    successful_datasets = 0
    failed_datasets = 0

    # Process both datasets
    for dataset_name, file_path in datasets.items():

        print("\n" + "=" * 50)
        print(f"PROCESSING: {dataset_name}")
        print("=" * 50)

        try:

            # 1. Load
            data = load_dataset(file_path)

            # 2. Inspect
            inspect_dataset(data, dataset_name)

            # 3. Clean
            data = clean_dataset(data)

            # 4. Remove duplicates
            data = remove_duplicates(data)

            # 5. Prepare
            data = prepare_dataset(data)

            # Create processed folder
            output_dir = DATASET_DIR / "Processed"
            output_dir.mkdir(exist_ok=True)

            # Save cleaned dataset
            output_name = file_path.stem + "_cleaned.csv"

            output_path = output_dir / output_name

            data.to_csv(output_path, index=False)

            print("\nProcessed dataset saved as:")
            print(output_path)

            successful_datasets += 1

        except Exception as error:

            print(f"\nError processing {dataset_name}: {error}")

            failed_datasets += 1

    # FINAL PROCESSING SUMMARY
    print("\n" + "=" * 50)
    print("DATASET PROCESSING SUMMARY")
    print("=" * 50)

    print("Successfully processed:", successful_datasets)
    print("Failed:", failed_datasets)

    if failed_datasets == 0:
        print("\nAll datasets processed successfully!")

    else:
        print("\nSome datasets could not be processed.")

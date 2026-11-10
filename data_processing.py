#todo: 1. Load the data
# 2. inspect the data
# 3. clean the data
# 4. Remove dupicates
# 5. prepare dataset


import pandas as pd


def load_dataset(file_path):

    data = pd.read_csv(file_path)

    print("Dataset loaded successfully!")
    print("Number of rows:", len(data))
    print("Number of columns:", len(data.columns))

    return data


def inspect_dataset(data):

    print("\nColumn Names:")
    print(data.columns.tolist())

    print("\nData Types:")
    print(data.dtypes)

    print("\nMissing Values:")
    print(data.isnull().sum())


if __name__ == "__main__":

    data = load_dataset("dataset/passwords.csv")

    inspect_dataset(data)

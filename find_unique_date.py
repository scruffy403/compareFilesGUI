import pandas as pd

# Define file paths (replace with your actual file paths)
file1_path = input("Please input the name of file 1: ")
file2_path = input("Please input the name of file 2: ")
output_file_path = input("Input the name for the output file: ")

# Read CSV files into DataFrames
df1 = pd.read_csv(file1_path)
df2 = pd.read_csv(file2_path)
unique_identifier = input("Input the column name you want to use as a unique identifier: ")

# Convert DataFrames to sets (assuming 'transactionID' is unique)
df1_set = set(df1[unique_identifier])
df2_unique_set = set(df2[unique_identifier]) - df1_set  # Difference between sets

# Filter df2 based on the unique set
df_not_in_1 = df2[df2[unique_identifier].isin(df2_unique_set)]

# Save the unique data to a new CSV file
df_not_in_1.to_csv(output_file_path, index=False)

print(f"Unique data from {file2_path} saved to {output_file_path}")
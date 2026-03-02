import pandas as pd

# Load the spreadsheet file
file_path = "input/30. KMDSZ Diáknapok - Csapatregisztráció (Responses).xlsx"
df = pd.read_excel(file_path)

# Make headers unique
unique_headers = {}
new_columns = []

for col in df.columns:
    base_col = col.rstrip(" .0123456789")  # Remove trailing spaces and numbers
    if base_col in unique_headers:
        unique_headers[base_col] += 1
        new_col_name = f"{base_col}.{unique_headers[base_col]}"
    else:
        unique_headers[base_col] = 0
        new_col_name = base_col
    new_columns.append(new_col_name)

df.columns = new_columns

# Save the modified file
output_file = "modified_sheet/Modified_Headers.xlsx"
df.to_excel(output_file, index=False)
print(f" Headers have been made unique and saved to {output_file}")

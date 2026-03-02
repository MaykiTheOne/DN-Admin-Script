import pandas as pd

# Load the file
file_path = "input/30. KMDSZ Diáknapok - Csapatregisztráció (Responses).xlsx"
df = pd.read_excel(file_path)

# Define the Csapatnev we are searching for
csapatnev = "Biolorgia"  # Replace with the actual team name

# Filter for the specific row where Csapatnev matches
filtered_df = df[df["Csapatnév:"] == csapatnev]

# If no matching row, exit
if filtered_df.empty:
    print(f"No matching team found for '{csapatnev}'.")
    exit()

# Define how many columns per member after skipping 22 fields
member_columns = 8

# Extract base columns
base_columns = ["Timestamp", "Csapatnév:"]

# Get all headers
all_headers = list(df.columns)

# Find where the member-specific columns start (ignoring first 22 after Csapatnev)
member_start_index = len(base_columns) + 22

# Create a new list to store transformed data
transformed_data = []

# Process the single matching row
row = filtered_df.iloc[0]
base_values = [row["Timestamp"], row["Csapatnév:"]]

# Process member data in chunks of 8 columns
for i in range(member_start_index, len(all_headers), member_columns):
    member_data = []
    for j in range(member_columns):
        col_index = i + j
        if col_index < len(all_headers):
            member_data.append(row[all_headers[col_index]])

    # Only add valid entries (ignoring empty ones)
    if any(pd.notna(member_data)):  
        transformed_data.append(base_values + member_data)

# Create new headers for the transformed table
new_headers = base_columns + all_headers[member_start_index : member_start_index + member_columns]
new_df = pd.DataFrame(transformed_data, columns=new_headers)

# Save to a new Excel file
output_file = f"output/{csapatnev}_Transformed.xlsx"
new_df.to_excel(output_file, index=False)

print(f"Data transformation complete! Saved as {output_file}")

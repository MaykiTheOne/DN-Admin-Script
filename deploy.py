#
# FBMark(Balázs) DN külön csapatokra embereket generáló scriptje(Cskt és AlCskt még nem tudja bevenni csak sima csapattagokat)
#
import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def process_file():
    # Ask user for the Excel file
    file_path = filedialog.askopenfilename(title="Valaszd ki az Excel filet(.xlsx)", filetypes=[("Excel Files", "*.xlsx")])
    if not file_path:
        return

    # Ask user for the team name
    csapatnev = team_entry.get().strip()
    if not csapatnev:
        messagebox.showerror("Error", "Adj meg egy csapatnevet!")
        return

    try:
        df = pd.read_excel(file_path)

        # Filter for the specific row where Csapatnev matches
        filtered_df = df[df["Csapatnév:"] == csapatnev]

        if filtered_df.empty:
            messagebox.showerror("Error", f"Nincs ilyen csapatnév '{csapatnev}'.")
            return

        # Define how many columns per member after skipping 22 fields
        member_columns = 8
        base_columns = ["Timestamp", "Csapatnév:"]
        all_headers = list(df.columns)
        member_start_index = len(base_columns) + 22

        # Process the single matching row
        row = filtered_df.iloc[0]
        base_values = [row["Timestamp"], row["Csapatnév:"]]
        transformed_data = []

        # Process member data in chunks of 8 columns
        for i in range(member_start_index, len(all_headers), member_columns):
            member_data = []
            for j in range(member_columns):
                col_index = i + j
                if col_index < len(all_headers):
                    member_data.append(row[all_headers[col_index]])

            if any(pd.notna(member_data)):  
                transformed_data.append(base_values + member_data)

        # Create new DataFrame
        new_headers = base_columns + all_headers[member_start_index : member_start_index + member_columns]
        new_df = pd.DataFrame(transformed_data, columns=new_headers)

        # Ensure output folder exists
        output_folder = "csapatok"
        os.makedirs(output_folder, exist_ok=True)  # Creates the folder if it doesn't exist

        # Save output file
        output_file = os.path.join(output_folder, f"{csapatnev}_feldolgozott.xlsx")
        new_df.to_excel(output_file, index=False)

        messagebox.showinfo("Success", f"Csapat feldolgozva!\nElmentve mint: {output_file}")

    except Exception as e:
        messagebox.showerror("Error", f"Hiba:\n{e}")

# GUI setup
root = tk.Tk()
root.title("DN Csapattagok szeparáló")

# Set window size to 600x300 pixels
root.geometry("600x300")

tk.Label(root, text="Add meg a csapatnevet pontosan ahogy a sheets-be van:", font=("Arial", 12)).pack(pady=10)
team_entry = tk.Entry(root, font=("Arial", 12), width=40)
team_entry.pack(pady=5)

tk.Button(root, text="Válaszd ki az Excel file-t és Dolgozd fel", command=process_file, font=("Arial", 12), width=30, height=2).pack(pady=20)

# Add small text in the lower-left corner
footer_label_left = tk.Label(root, text="Hajrá ADMIN !!!", font=("Trebuchet MS", 10, "bold"), fg="red", anchor="w")
footer_label_left.place(x=10, y=270)  # Positioned at bottom-left

# Add small text in the lower-right corner
footer_label_right = tk.Label(root, text="By: Kedvenc fotósotok", font=("Trebuchet MS", 10, "bold"), fg="red", anchor="e")
footer_label_right.place(x=460, y=270)  # Positioned at bottom-right

root.mainloop()

import sys
import os
import re
import pandas as pd
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel,
    QLineEdit, QPushButton, QFileDialog,
    QVBoxLayout, QMessageBox
)


class DNApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DN Csapattagok szeparáló")
        self.setMinimumWidth(500)

        layout = QVBoxLayout()

        self.label = QLabel("Add meg a csapatnevet pontosan ahogy a sheets-ben van:")
        layout.addWidget(self.label)

        self.team_input = QLineEdit()
        self.team_input.setPlaceholderText("Csapatnév...")
        layout.addWidget(self.team_input)

        self.button = QPushButton("Válaszd ki az Excel file-t és Dolgozd fel")
        self.button.clicked.connect(self.process_file)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def process_file(self):
        # ✅ Qt file dialog
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Valaszd ki az Excel filet(.xlsx)",
            "",
            "Excel Files (*.xlsx)"
        )

        if not file_path:
            return

        # ✅ Qt input mező
        csapatnev = self.team_input.text().strip()
        if not csapatnev:
            QMessageBox.critical(self, "Error", "Adj meg egy csapatnevet!")
            return

        try:
            df = pd.read_excel(file_path)

            filtered_df = df[df["Csapatnév:"] == csapatnev]

            if filtered_df.empty:
                QMessageBox.critical(self, "Error", f"Nincs ilyen csapatnév '{csapatnev}'.")
                return

            member_columns = 8
            base_columns = ["Csapatnév:"]
            all_headers = list(df.columns)
            member_start_index = len(base_columns) + 23

            row = filtered_df.iloc[0]
            base_values = [row["Csapatnév:"]]
            transformed_data = []

            for i in range(member_start_index, len(all_headers), member_columns):
                member_data = []
                for j in range(member_columns):
                    col_index = i + j
                    if col_index < len(all_headers):
                        member_data.append(row[all_headers[col_index]])

                # ✅ helyes any() használat
                # Ha a 3. oszlop (index 2) üres → ne vegyük fel
                if len(member_data) >= 3 and pd.notna(member_data[2]) and str(member_data[2]).strip() != "":
                    transformed_data.append(base_values + member_data)

            new_headers = base_columns + all_headers[
                member_start_index:member_start_index + member_columns
            ]

            new_df = pd.DataFrame(transformed_data, columns=new_headers)

            output_folder = "csapatok"
            os.makedirs(output_folder, exist_ok=True)

            output_file = os.path.join(output_folder, f"{csapatnev}_feldolgozott.xlsx")
            new_df.to_excel(output_file, index=False)

            QMessageBox.information(
                self,
                "Success",
                f"Csapat feldolgozva!\nElmentve mint: {output_file}"
            )

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Hiba:\n{e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DNApp()
    window.show()
    sys.exit(app.exec())
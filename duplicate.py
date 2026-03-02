import pandas as pd
import streamlit as st

st.title("Excel Column Duplicate Checker")

uploaded_file = st.file_uploader("Upload an Excel (.xlsx) file", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        st.success("File uploaded successfully!")

        st.write("### Available columns:")
        st.write(list(df.columns))

        column = st.selectbox("Select a column to check for duplicates in its rows", df.columns)

        if column:
            duplicate_values = df[column][df[column].duplicated(keep=False)]
            duplicate_rows = df[df[column].duplicated(keep=False)]

            if not duplicate_rows.empty:
                st.warning(f"Found {duplicate_values.nunique()} unique duplicated value(s) in column '{column}'")
                st.write("### Duplicate Rows:")
                st.dataframe(duplicate_rows)
            else:
                st.success(f"No duplicate values found in column '{column}'")

    except Exception as e:
        st.error(f"An error occurred: {e}")
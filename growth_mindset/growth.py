import streamlit as st
import pandas as pd
import os 
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout='wide')

# custom css
st.markdown(
    """
    <style>
    .stApp {
        background-color: black;
        color: white;
    }
    </style>
    """,
   unsafe_allow_html=True
)

# title and description
st.title("Data Sweeper")
st.write("This is a simple app to help you clean your data.")

# file uploader
uploaded_files = st.file_uploader("Choose a CSV or Excel file", type=["csv","xlsx"], accept_multiple_files=(True))

if uploaded_files is not None:
    for uploaded_file in uploaded_files:
        # read file
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("File type not supported. Please upload a CSV or Excel file.")
            continue

        # display file
        st.write("File: " + uploaded_file.name)
        st.dataframe(df.head())

        # data cleaning
        st.subheader("Data Cleaning")
        if st.checkbox(f"Clean data for{file.name}"):
            col1, col2 = st.columns(2)
            with col1:
                # remove duplicates
                if st.button("Remove duplicates"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates removed.")
            with col2:
                # fill missing values
                if st.button(f"Fill missing values for {file.name}"):
                    numeric_cols = df.select_dtypes(includes=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    df.dropna(inplace=True)
                    st.write("Missing values have been filled")

        st.subheader("Select Columns to Keep")
        columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]


        # data visualization
        st.subheader("Data Visualization")
        if st.checkbox(f"Show data visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # Conversion Options
        st.subheader("Conversion Options")
        conversion_type =st.radio(f"Convert {file.name} to:", ["CSV" , "Excel"], key=file.name)
        if st.button(f"Convert{file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to.csv(buffer, index=False)
                file_name = file.name.replace(file_ext,".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                buffer.seek(0)
           
           

        # download button
        st.download_button(
            label=f"Download {file.name} as {conversion_type}",
            data=buffer,
            file_name=file_name,
            mime=mime_type
        )

st.success("Thank you for using Data Sweeper!")
        
        

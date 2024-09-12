import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="terceros_fiscales"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        st.error(f"Error connecting to database: {e}")
        return None

def insert_data_to_db(connection, table_name, data):
    cursor = connection.cursor()
    sql = f"""
    INSERT INTO {table_name} (Nombre, NIT_C_C_, `Tipo de Régimen`, `Naturaleza Jurídica`, Dirección, Ciudad, `Teléfono/Celular`, Fax, Email)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    for i, row in data.iterrows():
        values = tuple(row.values)
        try:
            cursor.execute(sql, values)
            connection.commit()
        except Error as e:
            st.error(f"Error inserting data: {e}")

def process_uploaded_files(files):
    data_frames = []
    for file in files:
        data = pd.read_excel(file)
        st.write(f"Data from {file.name}:")
        st.dataframe(data)
        data_frames.append(data)
    return data_frames

def combine_and_insert_tables(data_frames, table_name):
    if not data_frames:
        st.warning("No data frames to combine.")
        return
    
    combined_data = pd.concat(data_frames, ignore_index=True)
    st.write("Combined Data:")
    st.dataframe(combined_data)
    
    connection = create_connection()
    if connection:
        insert_data_to_db(connection, table_name, combined_data)
        connection.close()

st.title("Upload Excel Files to MySQL Tables")

table_option = st.selectbox(
    "Select the table where the combined data will be inserted",
    ["clientes", "otros_terceros", "proveedores"]
)

uploaded_files = st.file_uploader("Upload Excel file(s)", accept_multiple_files=True, type=["xlsx"])

if uploaded_files:
    data_frames = process_uploaded_files(uploaded_files)
    
    if st.button("Combine and Insert Tables"):
        combine_and_insert_tables(data_frames, table_option)

st.write("Made by: Sergio Marín Giraldo")
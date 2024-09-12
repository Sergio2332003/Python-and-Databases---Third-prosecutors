import os
import streamlit as st
import mysql.connector
from mysql.connector import Error

st.title("Verify connection to database")

verify = st.button("Verify")

if verify:
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),   
        password='',
        database=os.getenv("DB_NAME")
    )
    try:
        if connection.is_connected():
            st.write("Conexión exitosa a la base de datos MySQL")

            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            st.write(f"Conectado a la base de datos: {record[0]}")

    except Error as e:
        st.write(f"Error al conectar a MySQL: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            st.write("Conexión MySQL cerrada")
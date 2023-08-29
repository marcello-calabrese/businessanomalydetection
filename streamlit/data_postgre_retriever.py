import psycopg2
import pandas as pd
import streamlit as st
#from conn_string import CONN_STRING



# function to load the data from the elephantSQL database
@st.cache_resource
def retrieve_data_to_dataframe(connection_string, query):
    try:
        conn = psycopg2.connect(connection_string)
        df = pd.read_sql_query(query, conn)
        print("Data retrieved successfully.")

        return df

    except Exception as e:
        print("An error occurred:", e)

    finally:
        if conn:
            conn.close()
            
# test the function

# query = 'SELECT * FROM anomaly_detection'

# df = retrieve_data_to_dataframe(CONN_STRING, query)

# print(df.head())
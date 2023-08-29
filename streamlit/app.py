import streamlit as st
import pandas as pd
from PIL import Image
from conn_string import CONN_STRING
from data_postgre_retriever import retrieve_data_to_dataframe
from predict_model import predict_anomalies
import plotly.express as px

st.set_page_config(page_title="Anomaly Detection", page_icon=":shark:", layout="wide", initial_sidebar_state="expanded")

with open("style.css") as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)
st.title("Anomaly Detection")

st.write("This app is a simple demonstration of how to use Streamlit as dashboard to build a web app that connects to a PostgreSQL database, runs the Anomaly Detection and displays the data.")

st.success("Screenshot of the data stored in the ElephantSQL PostgreSQL database")

image = Image.open('img/db_sql.JPG')

st.image(image, caption='Data stored in the ElephantSQL PostgreSQL database', width=1200)

query = 'SELECT * FROM anomaly_detection'

df = retrieve_data_to_dataframe(CONN_STRING, query)



# create a sidebar with 3 options to display the data: General, Basic Stats, Model Stats 

st.sidebar.title("Display Options") # title for the sidebar
# create a list of options
options = ["General", "Anomaly Model Implementation and Dashboard"]
# create a selectbox to display the options
choice = st.sidebar.selectbox("Select an option", options)
# create a checkbox to display the data

if choice == "General":
    st.write("This is the general data.")
    st.dataframe(df.head(), hide_index=True)

   
elif choice == "Anomaly Model Implementation and Dashboard":
    st.title("Anomaly Model Implementation and Dashboard")
    st.write("This is the anomaly model implementation and dashboard. The model used is Isolation Forest. The library used is PyCaret.")
    st.success("Time to predict the anomalies!")
    # create a button to predict the anomalies
    if st.button("Predict Anomalies"):
        # call the predict_anomalies function from predict_model.py
        predictions = predict_anomalies(df)
        # display the predictions
        st.success("**Predictions are ready!**")
        st.markdown("#### Summary of the Anomalies (0: no anomaly, 1: anomaly) and Anomaly Scores (the lower the score, the more anomalous the data)")
        st.dataframe(predictions, hide_index=True)
        # create a button to display the dashboard
        
        # display the dashboard
        st.success("**Below we can see the original dataset with the Anomaly and Anomaly_Score columns added.**")
        # add the Anomaly and Anomaly_Score columns to the dataframe
        df['Anomaly'] = predictions['Anomaly']
        df['Anomaly_Score'] = predictions['Anomaly_Score']
        # display the dataframe
        st.dataframe(df, hide_index=True)
        # create a ruler separating the dataframe from the dashboard
        st.markdown("-------------------------------------------------------------------------------------")
        # Dashboard area
        st.title(" :bar_chart: Sample SuperStore EDA")
        # create 3 rows and 3 columns
        # Add custom CSS to create horizontal spacing
        st.markdown(
            """
            <style>
                .custom-columns {
                    display: flex;
                    justify-content: space-between;
                    margin: 0 -40px;
                    padding-top: 20px;
                    padding-right: 20px;
                    padding-left: 20px;
                }
                .custom-col {
                    flex: 1;
                    padding: 0 40px;
                    padding-top: 20px;
                    padding-right: 20px;
                    padding-left: 20px;
                }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Create a container for the columns
        col_container = st.container()

        # Use the container to create columns with custom styling
        with col_container:
            col1, col2, col3 = st.columns(3, gap='medium')
            
            # Create a st.metric to display the total sales and total profit showing only 2 decimal places
            with col1:
                st.metric(label="Total Sales", value=f"${df['sales'].sum():,.2f}")
                # Create a bar chart to display the total sales by region
                fig1 = px.bar(df, x='region', y='sales', color='region', title='Total Sales by Region')
                st.plotly_chart(fig1, use_container_width=True)
                # show a bar chart to display the total count of the column 'Anomaly'
                fig4 = px.bar(df['Anomaly'].value_counts(ascending=False), x='Anomaly', title='Total Count of Anomalies')
                st.plotly_chart(fig4, use_container_width=True)
            
            with col2:
                st.metric(label="Total Profit", value=f"${df['profit'].sum():,.2f}")
                # Create a bar chart to display the total sales by category
                fig2 = px.bar(df, x='category', y='sales', color='category', title='Total Sales by Category')
                st.plotly_chart(fig2, use_container_width=True)
                # display a chart with regions and the total count of anomalies by region
                fig5 = px.bar(df.groupby('region')['Anomaly'].sum().sort_values(ascending=True), x='Anomaly', title='Total Anomalies by Region')
                st.plotly_chart(fig5, use_container_width=True)
            
            with col3:
                st.metric(label="Total Quantity", value=f"{df['quantity'].sum():,}")
                # create a a bar chart to display the total quantity by sold by sub-category
                fig3 = px.bar(df, x='sub_category', y='quantity', color='sub_category', title='Total Quantity by Sub-Category')
                st.plotly_chart(fig3, use_container_width=True)
                 # display a chart with regions and the total count of anomalies by region
                fig6 = px.bar(df.groupby('sub_category')['Anomaly'].sum().sort_values(ascending=True), x='Anomaly', title='Total Anomalies by Product')
                st.plotly_chart(fig6, use_container_width=True)
                
        # show the dataframe with with color gradient based on the Anomaly_Score
        st.markdown("-------------------------------------------------------------------------------------")
        # create a container to display the dataframe with Anomaly equal to 1
        st.success(" **Dataset containing only the anomalies**s")
        # create a dataframe with Anomaly equal to 1
        df_anomalies = df[df['Anomaly'] == 1]
        # display the dataframe
        st.dataframe(df_anomalies, hide_index=True)
        


        

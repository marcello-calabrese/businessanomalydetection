from pycaret.anomaly import predict_model, load_model
from conn_string import CONN_STRING
import streamlit as st


# create a function that loads the model and predicts anomalies using pycaret
@st.cache_resource
def predict_anomalies(df, model_name='C:/Users/marce/Desktop/Python/pythoncheatsheets/python_projects/businessanomalydetection/model_training/iforest_model'):
    # load the model
    model = load_model(model_name)
    # predict the anomalies
    predictions = predict_model(model, data=df)
    # return the predictions
    return predictions


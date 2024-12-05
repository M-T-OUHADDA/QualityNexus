import streamlit as st
import pandas as pd
import numpy as np
from pycaret.regression import *
from pycaret.classification import *
import os

models_path = 'models'
features_dict = {
    'ProductionCost': ["ProductionVolume", "DefectStatus", "SupplierQuality", "DeliveryDelay", "DefectRate", "QualityScore", "MaintenanceHours", "DowntimePercentage", "InventoryTurnover", "StockoutRate", "WorkerProductivity", "SafetyIncidents", "EnergyConsumption", "EnergyEfficiency", "AdditiveProcessTime", "AdditiveMaterialCost"],

    'DeliveryDelay': ["ProductionVolume", "ProductionCost", "SupplierQuality", "DefectStatus", "DefectRate", "QualityScore", "MaintenanceHours", "DowntimePercentage", "InventoryTurnover", "StockoutRate", "WorkerProductivity", "SafetyIncidents", "EnergyConsumption", "EnergyEfficiency", "AdditiveProcessTime", "AdditiveMaterialCost"],

    'DefectRate': ['ProductionVolume', 'SupplierQuality', 'MaintenanceHours', 'WorkerProductivity'],
    'QualityScore': ['SupplierQuality', 'DefectRate', 'MaintenanceHours', 'WorkerProductivity'],
    'InventoryTurnover': ['ProductionVolume', 'DeliveryDelay', 'QualityScore'],
    'StockoutRate': ['InventoryTurnover', 'DeliveryDelay'],
    'SafetyIncidents': ['DefectRate'], #Data
    'EnergyConsumption': ['DefectRate', 'ProductionVolume', 'SupplierQuality', 'MaintenanceHours', 'DowntimePercentage', 'InventoryTurnover', 'WorkerProductivity', 'SafetyIncidents', 'EnergyEfficiency', 'AdditiveProcessTime'],
    'DefectStatus': ["ProductionVolume", "ProductionCost", "SupplierQuality", "DeliveryDelay", "DefectRate", "QualityScore", "MaintenanceHours", "DowntimePercentage", "InventoryTurnover", "StockoutRate", "WorkerProductivity", "SafetyIncidents", "EnergyConsumption", "EnergyEfficiency", "AdditiveProcessTime", "AdditiveMaterialCost"]

}


# Function to load models
def load_models(models_path):
    models = [f for f in os.listdir(models_path) if f.endswith('.pkl')]
    return models

# Function to get the model based on the selection
def load_selected_model(models_path, selected_model_name):
    mdl_name = ''.join(selected_model_name.split())
    model_path = os.path.join(models_path, mdl_name)
    try:
        model = load_model(model_path)
    except Exception as e:
        st.write(model_path)
        st.write(f"Error loading model: {e}")
    return model

# Convert to Title Case with spaces
def to_title_with_spaces(string):
    return ''.join([' ' + char if char.isupper() else char for char in string]).strip().title()
# Function to create the prediction input form
def get_input_form(selected_model_name, input_form):
    # pascal format
    mdl = ''.join(selected_model_name.split())
    features = features_dict.get(mdl).copy()
    values = []
    depencies_num = len(features)
    if input_form == 'Input Edit':
        cols = st.columns(3)
        itr = 0
        while features:
            itr %= 3
            with cols[itr]:
                if "Efficiency" in features[0]:
                    val = st.slider(features[0], min_value=0.0, max_value=1.0, step=0.01)
                    st.markdown("<hr style='margin: 0;'>", unsafe_allow_html=True)
                elif features[0] == "StockoutRate":
                    val = st.number_input(features[0], step=0.0001, min_value=0.0, max_value=0.02, format="%.6f")
                    st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)
                elif "Status" in features[0]:
                    val = {'Yes':1, 'No':0}[st.selectbox(features[0], ["Yes", "No"])]
                elif "Percentage" in features[0] or "Quality" in features[0] or features[0] == "WorkerProductivity":
                    val = st.slider(features[0], min_value=0.0, max_value=100.0, step=0.01)
                    st.markdown("<hr style='margin: 0;'>", unsafe_allow_html=True)
                elif features[0] in ["ProductionVolume", "DeliveryDelay", "SafetyIncidents"]:
                    val = st.number_input(features[0], step=1, min_value=0)
                    st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)
                else:
                    val = st.number_input(features[0], step=0.1, help ="wojqoijda", format="%.6f")
                    st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)
                values.append(val)
                features.pop(0)
            itr += 1
        try:
            return pd.DataFrame([values], columns=features_dict[mdl])
        except Exception as ex:
            st.write(ex)
    elif input_form == 'Data Upload':
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        if uploaded_file is not None:
            st.write('The Head of Uploaded Data')
            dr = pd.read_csv(uploaded_file)
            dr = dr[features_dict[mdl]]
            st.dataframe(dr.head())
            return dr
    elif input_form == 'Data Frame':
        df = pd.DataFrame([[0 for i in range(depencies_num)]], columns=features_dict[mdl])
        edited_df = st.data_editor(df, num_rows='dynamic', column_config={col: st.column_config.NumberColumn(format="%0.6f") for col in df.columns})
        return edited_df
def main():
    # Page Setup
    st.set_page_config(
        page_title="Quality Nexus", 
        page_icon="res/icon.png",
        layout="wide" 
    )

    # Title
    st.title("Quality Nexus: Industrial Tool")

    # Description
    st.write(
        """
        This app is a tool that helps with predicting some features
        """)

    # Models
    available_models = load_models(models_path)

    # Feature Selection
    feature = st.sidebar.selectbox('Choose an parameter to predict:',
        [to_title_with_spaces(mdl.removesuffix('.pkl')) for mdl in available_models])

    if feature:
        model = load_selected_model(models_path, feature)

        input_form = st.sidebar.radio('Input Form', ['Input Edit', 'Data Upload', 'Data Frame'])
        input_data = get_input_form(feature, input_form)

        if st.button("Get Prediction"):
            # Get prediction using PyCaret
            prediction = predict_model(model, data=input_data)
            st.dataframe(prediction)
            if 'prediction_score' in prediction:
                st.write(f"The Confidence to be Defected is: {prediction['prediction_score'][0] * 100}%")
                st.header(f"Prediction: {['Not Defected', 'Defected'][prediction['prediction_label'][0]]}")
            else:
                st.metric(label="Prediction", value=prediction['prediction_label'][0])

        

        selections = st.sidebar.multiselect("Visualisations ", options= ['Graphs'])
        #graph_color = st.sidebar.color_picker("Colors")
        if st.button("Save Log"):
            st.tab()



if __name__ == "__main__":
    main()
    today = pd.to_datetime("today")
    version = "Version 3.6.0 Zakaria NAJI, Mohamed OUHADDA " + str(today)[:-7] 
    st.markdown(version)

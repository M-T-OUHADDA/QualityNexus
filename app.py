import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from pycaret.regression import *
from pycaret.classification import *
import plotly.express as px
import os

models_path = 'models'
features_dict = {
    'ProductionCost': ['ProductionVolume', 'SupplierQuality', 'DefectRate', 'QualityScore', 'EnergyConsumption', 'AdditiveProcessTime', 'AdditiveMaterialCost'],
    'DeliveryDelay': ['DefectRate', 'MaintenanceHours', 'DowntimePercentage', 'StockoutRate', 'WorkerProductivity', 'SafetyIncidents', 'AdditiveProcessTime', 'DefectStatus'],
    'DefectRate': ['ProductionVolume', 'SupplierQuality', 'MaintenanceHours', 'WorkerProductivity'],
    'QualityScore': ['SupplierQuality', 'DefectRate', 'MaintenanceHours', 'WorkerProductivity'],
    'InventoryTurnover': ['ProductionVolume', 'DeliveryDelay', 'QualityScore'],
    'StockoutRate': ['InventoryTurnover', 'DeliveryDelay'],
    'SafetyIncidents': ['DefectRate'], #Data
    'EnergyConsumption': ['DefectRate', 'ProductionVolume', 'SupplierQuality', 'MaintenanceHours', 'DowntimePercentage', 'InventoryTurnover', 'WorkerProductivity', 'SafetyIncidents', 'EnergyEfficiency', 'AdditiveProcessTime'],
    'DefectStatus': ["ProductionVolume", "ProductionCost", "SupplierQuality", "DeliveryDelay", "DefectRate", "QualityScore", "MaintenanceHours", "DowntimePercentage", "InventoryTurnover", "StockoutRate", "WorkerProductivity", "SafetyIncidents", "EnergyConsumption", "EnergyEfficiency", "AdditiveProcessTime", "AdditiveMaterialCost"]

}

def handle_production_volume():
    val = st.number_input("Production Volume", step=50, min_value=1, help="The total amount of product units that are manufactured, impacting scale and efficiency.")
    st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)
    return val

def handle_production_cost():
    val = st.number_input("Production Cost", step=0.1, help="The monetary expenses involved in producing a single unit, a key driver of profitability.", format="%.6f")
    st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)
    return val

def handle_supplier_quality():
    val = st.slider("Supplier Quality", min_value=0.0, max_value=100.0, step=0.01, help="A measure of raw materials or component excellence, influencing final product standards.")
    st.markdown("<hr style='margin: 0;'>", unsafe_allow_html=True)
    return val

def handle_delivery_delay():
    val = st.number_input("Delivery Delay", step=1, min_value=0, help="The lag time from order to arrival, crucial for planning and just-in-time operations.")
    st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)
    return val

def handle_defect_rate():
    val = st.slider("Defect Rate", min_value=0.0, max_value=100.0, step=0.01, help="The percentage of manufactured products failing quality checks, indicating process effectiveness.")
    st.markdown("<hr style='margin: 0;'>", unsafe_allow_html=True)
    return val

def handle_quality_score():
    val = st.slider("Quality Score", min_value=0.0, max_value=100.0, step=0.01, help="An overall measure of product quality, reflecting adherence to standards and customer satisfaction.")
    st.markdown("<hr style='margin: 0;'>", unsafe_allow_html=True)
    return val

def handle_maintenance_hours():
    val = st.number_input("Maintenance Hours", step=0.1, help="The time allocated for machinery upkeep, influencing operational continuity and reliability.", format="%.6f")
    st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)
    return val

def handle_downtime_percentage():
    val = st.slider("Downtime Percentage", min_value=0.0, max_value=100.0, step=0.01, help="The fraction of time equipment is non-operational, impacting output and deadlines.")
    st.markdown("<hr style='margin: 0;'>", unsafe_allow_html=True)
    return val

def handle_inventory_turnover():
    val = st.number_input("Inventory Turnover", step=0.1, help="How quickly stock is sold or used, a sign of efficiency in managing materials.", format="%.6f")
    st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)
    return val

def handle_stockout_rate():
    val = st.number_input("Stockout Rate", step=0.0001, min_value=0.0, max_value=0.02, format="%.6f", help="The probability of not having sufficient inventory when needed, risking production delays or lost sales.")
    st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)
    return val

def handle_worker_productivity():
    val = st.slider("Worker Productivity", min_value=0.0, max_value=100.0, step=0.01, help="A measure of employee efficiency and output, indicating operational labor effectiveness.")
    st.markdown("<hr style='margin: 0;'>", unsafe_allow_html=True)
    return val

def handle_safety_incidents():
    val = st.number_input("Safety Incidents", step=1, min_value=0, help="The quantity of workplace accidents, a vital measure of a healthy and safe environment.")
    st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)
    return val

def handle_energy_consumption():
    val = st.number_input("Energy Consumption", step=0.1, help="Total energy used during production, a key factor in sustainability and cost management.", format="%.6f")
    st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)
    return val

def handle_energy_efficiency():
    val = st.slider("Energy Efficiency", min_value=0.0, max_value=1.0, step=0.01, help="The ratio of useful output to energy input, reflecting how well resources are utilized.")
    st.markdown("<hr style='margin: 0;'>", unsafe_allow_html=True)
    return val

def handle_additive_process_time():
    val = st.number_input("Additive ProcessTime", step=0.1, help="The time taken for additive manufacturing processes, important for understanding production flow.", format="%.6f")
    st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)
    return val

def handle_additive_material_cost():
    val = st.number_input("Additive MaterialCost", step=0.1, help="The expense of the raw materials used in additive processes, a key element of cost analysis.", format="%.6f")
    st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)
    return val

def handle_defect_status():
    val = {'Yes': 1, 'No': 0}[st.selectbox("Defect Status", ["Yes", "No"], help="Indicates whether any products are defective, a crucial aspect of quality control.")]# Function to load models
    return val

def load_models(models_path):
    models = [f for f in os.listdir(models_path) if f.endswith('.pkl')]
    return models

#Mapping features and their handle functions
handlers = {
    "ProductionVolume": handle_production_volume,
    "ProductionCost": handle_production_cost,
    "SupplierQuality": handle_supplier_quality,
    "DeliveryDelay": handle_delivery_delay,
    "DefectRate": handle_defect_rate,
    "QualityScore": handle_quality_score,
    "MaintenanceHours": handle_maintenance_hours,
    "DowntimePercentage": handle_downtime_percentage,
    "InventoryTurnover": handle_inventory_turnover,
    "StockoutRate": handle_stockout_rate,
    "WorkerProductivity": handle_worker_productivity,
    "SafetyIncidents": handle_safety_incidents,
    "EnergyConsumption": handle_energy_consumption,
    "EnergyEfficiency": handle_energy_efficiency,
    "AdditiveProcessTime": handle_additive_process_time,
    "AdditiveMaterialCost": handle_additive_material_cost,
    "DefectStatus": handle_defect_status
}

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
                handler = handlers.get(features[0])
                if handler:
                    val = handler()
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
        This app is a tool that helps with predicting some industrial feautures
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
        final_frame = None 
        if st.button("Get Prediction"):
            # Get prediction using PyCaret
            prediction = predict_model(model, data=input_data)
            final_frame = st.dataframe(prediction)
            if 'prediction_score' in prediction:
                st.write(f"The Confidence to be Defected is: {prediction['prediction_score'][0] * 100}%")
                st.header(f"Prediction: {['Not Defected', 'Defected'][prediction['prediction_label'][0]]}")
            else:
                st.metric(label="First Prediction", value=prediction['prediction_label'][0])

        
        if input_form == "Data Upload" or input_form == "Data Frame" :
            selections = st.sidebar.multiselect("Visualizations",
                                                options=['Bar Graph', 
                                                         'Line Graph', 
                                                         'Scatter Plot', 
                                                         'Pie Chart', 
                                                         'Area Chart', 
                                                         'Histogram', 
                                                         'Heatmap', 
                                                         'Bubble Chart',
                                                         'Aggregations'])
            if len(selections) == 1 and "Aggregations" in selections:
                pass
            else:
                # Check if 'Graphs' is selected
                graph_merge = st.sidebar.radio("Select Graphs Merging Staus", ['Not Merged', 'Merged'
    ])
        
                #Color Picker for customizing the graph color
                colors = {} 
                for graph in selections:
                    if graph != "Aggregations":
                        graph_color = st.sidebar.color_picker(f"Choose {graph} Color", '#3561EC')
                        colors[graph] = graph_color

                if isinstance(input_data, pd.DataFrame) and final_frame is not None:
                    prediction_labels = prediction['prediction_label'].tolist()
                    row_indexes = list(range(len(prediction_labels)))
                    graphs = []
                    #Create graphs based on the selected graphs
                    # Bar Graph
                    if 'Bar Graph' in selections:
                        graph_color = colors['Bar Graph']
                        bar_graph = px.bar(x=row_indexes, y=prediction_labels,
                            color_discrete_sequence=[graph_color] if graph_color else ['#ADD8E6'],
                            labels={'x': 'Row Index', 'y': 'Prediction Label'}
                        )
                        graphs.append(bar_graph)

                    # Line Graph
                    if 'Line Graph' in selections:
                        graph_color = colors['Line Graph']
                        line_graph = px.line(x=row_indexes, y=prediction_labels,
                            color_discrete_sequence=[graph_color] if graph_color else ['#ADD8E6'],
                            labels={'x': 'Row Index', 'y': 'Prediction Label'}
                        )
                        graphs.append(line_graph)

                    # Scatter Plot
                    if 'Scatter Plot' in selections:
                        graph_color = colors['Scatter Plot']
                        scatter_plot = px.scatter(x=row_indexes, y=prediction_labels,
                            color_discrete_sequence=[graph_color] if graph_color else ['#ADD8E6'],
                            labels={'x': 'Row Index', 'y': 'Prediction Label'}
                        )
                        graphs.append(scatter_plot)

                    # Pie Chart
                    if 'Pie Chart' in selections:
                        graph_color = colors['Pie Chart']
                        pie_chart = px.pie(names=row_indexes, values=prediction_labels,
                            color_discrete_sequence=[graph_color] if graph_color else ['#ADD8E6'],
                            labels={'names': 'Row Index', 'values': 'Prediction Label'}
                        )
                        graphs.append(pie_chart)

                    # Area Chart
                    if 'Area Chart' in selections:
                        graph_color = colors['Area Chart']
                        area_chart = px.area(x=row_indexes, y=prediction_labels,
                            color_discrete_sequence=[graph_color] if graph_color else ['#ADD8E6'],
                            labels={'x': 'Row Index', 'y': 'Prediction Label'}
                        )
                        graphs.append(area_chart)

                    # Histogram
                    if 'Histogram' in selections:
                        graph_color = colors['Histogram']
                        histogram = px.histogram(x=prediction_labels,
                            color_discrete_sequence=[graph_color] if graph_color else ['#ADD8E6'],
                            labels={'x': 'Prediction Label', 'y': 'Count'}
                        )
                        graphs.append(histogram)

                    # Heatmap
                    if 'Heatmap' in selections:
                        heatmap = px.imshow(input_data.corr(), color_continuous_scale='Viridis',
                            labels={'x': 'Features', 'y': 'Features'}
                        )
                        graphs.append(heatmap)

                    # Bubble Chart
                    if 'Bubble Chart' in selections:
                        graph_color = colors['Bubble Chart']
                        bubble_size = [i * 10 for i in range(len(prediction_labels))]  # Example: Bubble sizes
                        bubble_chart = px.scatter(x=row_indexes, y=prediction_labels, size=bubble_size,
                            color_discrete_sequence=[graph_color] if graph_color else ['#ADD8E6'],
                            labels={'x': 'Row Index', 'y': 'Prediction Label'}
                        )
                        graphs.append(bubble_chart)
                                                                                             
                    #Display the selected graph
                    if graph_merge == "Merged":
                        fig = go.Figure()
                        for graph in graphs:
                            for trace in graph['data']:
                                fig.add_trace(trace)
                        fig.update_layout(
                            title="Merged Graphs",
                            xaxis_title="X Axis",
                            yaxis_title="Y Axis",
                            showlegend=True  # To show legends for different traces
                        )
                        st.plotly_chart(fig)        
                    else:                          

                        for fig in graphs:
                            fig.update_layout(
                                xaxis=dict(
                                    tickmode='linear',  # Ensure that the ticks are linear (not categorical)
                                    dtick=1,  # Set the step between ticks to 1 (integer values)
                                    tick0=0  # Start ticks at 0
                                    )
                                )   
                            st.plotly_chart(fig)   
            if "Aggregations" in selections:
                if isinstance(input_data, pd.DataFrame):
                    st.subheader("Aggregated Data:")
                    st.write(input_data.agg(['sum', 'mean', 'median', 'std', 'min', 'max']))     
        if st.button("Save Log"):
            st.tab()



if __name__ == "__main__":
    main()
    today = pd.to_datetime("today")
    version = "Version 3.6.0 Zakaria NAJI, Mohamed OUHADDA " + str(today)[:-7] 
    st.markdown(version)

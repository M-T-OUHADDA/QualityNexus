import streamlit as st
import os
from pycaret.regression import load_model, evaluate_model
from pycaret.classification import load_model as load_classification_model, evaluate_model as evaluate_classification_model
import graphviz
import pandas as pd
models_path = 'models'
available_models = [f for f in os.listdir(models_path) if f.endswith('.pkl')]
def load_selected_model(models_path, selected_model_name):
    model_path = os.path.join(models_path, selected_model_name.removesuffix('.pkl'))

    try:
        model = load_model(model_path)
    except:
        model = load_classification_model(model_path)
    return model

def get_feature_flow_graph(model, target_variable, model_name):
    dot = graphviz.Digraph(comment='Feature Flow', graph_attr={'rankdir': 'LR'})
    
    if hasattr(model, 'feature_names_in_'):
        features = model.feature_names_in_
        features.remove(model_name)
    elif hasattr(model, 'get_booster') and hasattr(model.get_booster(), 'feature_names'):
        features = model.get_booster().feature_names
        features.remove(model_name)
    else:
        features = []
    st.write(features)
    for feature in features:
        dot.node(feature, label=feature)
    dot.node(target_variable, label=target_variable, shape='box', style='filled', fillcolor='lightskyblue')
    dot.node(model_name, label= 'predicted '+model_name, shape='box', style='filled', fillcolor='#FF5B61')
 
    for feature in features:
        dot.edge(feature, target_variable)

    dot.edge(target_variable, model_name)



    return dot

st.sidebar.title("Model Inspect")
selected_model_name = st.sidebar.selectbox('Select a Model:', available_models)

if selected_model_name:
    model = load_selected_model(models_path, selected_model_name)


    if hasattr(model, 'target_name'):
        target_variable = model.target_name
    else:
        target_variable = 'Trained Model'
    model_name = selected_model_name.removesuffix('.pkl')
    graph = get_feature_flow_graph(model, target_variable, model_name)
    st.graphviz_chart(graph)

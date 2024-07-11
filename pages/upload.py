import streamlit as st
import time
import os
import json
import pandas as pd
from classes.cv import cv
import asyncio
import datetime

# Page configuration
st.markdown("# Upload CV ❄️")
st.sidebar.markdown("# Upload CV ❄️")

# Function to print and display data from JSON
def print_data(json_data):
    df = pd.DataFrame()
    latest_iteration = st.empty()
    bar = st.progress(0)
    if isinstance(json_data, dict):
        i = 1
        j = len(json_data.items())
        for cle, valeur in json_data.items():
            if isinstance(valeur, list):
                df[cle] = pd.Series([valeur])
                st.text(cle + ":")  
                st.data_editor(data=valeur, column_config={cle: {"dataname": cle}}, key=cle, use_container_width=True, num_rows="dynamic")
            elif isinstance(valeur, str):
                st.text_area(cle + ":", valeur, key=cle, label_visibility="visible")
            elif isinstance(valeur, dict):
                print_data(valeur)
            else:
                pass
            latest_iteration.text(f'Iteration {i}')
            bar.progress(i / j)
            time.sleep(0.1)
            i += 1
            df[cle] = pd.Series([valeur])
        return df

# Function to save data back to JSON
def save_data(json_data):
    if isinstance(json_data, dict):
        for cle in json_data.keys():
            if isinstance(json_data[cle], list):
                edited_list = st.session_state[cle]["edited_rows"]               
                for key, sub_dict in edited_list.items():
                    json_data[cle][key] = sub_dict.get("value")
            elif isinstance(json_data[cle], str):
                json_data[cle] = st.session_state[cle]
        with open(f"data/{datetime.datetime.now().strftime('%d%m%y_%H%M%S')}.json", 'w') as outfile:
            json.dump(json_data, outfile)

# File uploader
json_data=None
file = st.file_uploader('Select a file', type=['json', 'pdf'])
if file is not None and json_data is  None:
    if file.name.endswith(".json"):
        file_contents = file.read()
        json_data = json.loads(file_contents)
        df = print_data(json_data)
        
    elif file.name.endswith(".pdf"):
        with open(f"CV/{file.name}", 'wb') as f:
            f.write(file.read())
            saved_file_path = os.path.abspath(file.name)
        cvdata = cv(saved_file_path)
        asyncio.run(cvdata.toict())
        json_data = json.loads(cvdata.json_data)
        json_data["CV File path"] = f"CV/{file.name}"
        df = print_data(json_data)

    # Submit button
if json_data is not None:
    submitted = st.button(label='Soumettre')
    if submitted:
        save_data(json_data)
        json_data=None

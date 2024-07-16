import streamlit as st
import time
import os
from pathlib import Path
import json
import pandas as pd
from sympy import true
from classes.cv import cv
import asyncio
import datetime
import base64

def app():
    #st.set_page_config(layout="wide")
    st.markdown("# Upload CV ❄️")
    #st.sidebar.markdown("# Upload CV ❄️")
    data={}
    # Function to print and display data from JSON
    def print_data(json_data):
        df = pd.DataFrame()
        latest_iteration = st.empty()
        bar = st.progress(0)
        if isinstance(json_data, dict):
            i = 1
            j = len(json_data.items())
            for key, value in json_data.items():
                if isinstance(value, list):
                    df[key] = pd.Series([value])
                    st.text(key + ":")
                    data[key] = st.data_editor(data=value, column_config={key: {"dataname": key}}, key=key, use_container_width=True, num_rows="dynamic")
                elif isinstance(value, str):
                    data[key] =st.text_area(key + ":", value, key=key, label_visibility="visible")
                elif isinstance(value, dict):
                    print_data(value)
                else:
                    pass
                latest_iteration.text(f'Iteration {i}')
                bar.progress(i / j)
                time.sleep(0.1)
                i += 1
        return data

    # Function to save data back to JSON
    def save_data(jdata,path):
        jdata["PDF_CV_PATH"]=path
        output_dir = Path("../../jobfit/resources/data")
        with open(f"../../jobfit/resources/data/{datetime.datetime.now().strftime('%d%m%y_%H%M%S')}.json", 'w') as outfile:
            json.dump(jdata, outfile)

    def openfile(file):
        if file.name.endswith(".json"):
            file_contents = file.read()
            json_data = json.loads(file_contents)
            cv_filename = ""
        elif file.name.endswith(".pdf"):
            output_dir = Path("resources/CV")
            with open(f"../../jobfit/resources/CV/{file.name}", 'wb') as f:
                f.write(file.read())
                saved_file_path = os.path.abspath(f"CV/{file.name}")
            with open("uploaded_file.pdf", "wb") as f:
                f.write(file.getbuffer())        
            with open("uploaded_file.pdf", "rb") as f:
                st.session_state.base64_pdf = base64.b64encode(f.read()).decode('utf-8')
            
            
            cvdata = cv(saved_file_path)
            asyncio.run(cvdata.toict())
            json_data = json.loads(cvdata.json_data)
            cv_filename = f"jobfit/resources/CV/{file.name}"
        st.session_state.json_data = json_data
        st.session_state.cv_filename=cv_filename
        st.session_state.data=print_data(st.session_state.json_data)
    file = st.file_uploader('Select a file', type=['json', 'pdf'])
    col1, col2 = st.columns(2)
    with col1:    
        #if 'json_data' not in st.session_state:    
        if file :
            if "data" not in st.session_state:
                with st.spinner('In progress...'):
                    openfile(file)
            

        # Every form must have a submit button.
        submitted = st.button("Submit")
        if submitted:
            save_data(st.session_state.data,st.session_state.cv_filename)
            st.session_state.pop("data")
            st.success("CV Data Saved successfully")


    with col2:
        if "base64_pdf" in st.session_state:
            pdf_display = F'<iframe src="data:application/pdf;base64,{st.session_state.base64_pdf}" width="900" height="1500" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)    


if __name__ == "__main__":
    app()
    

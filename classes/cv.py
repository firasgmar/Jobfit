from pdfminer.high_level import extract_text
import asyncio
from ollama import Client
from ollama import AsyncClient
import ollama
import json
import re
import os
from pathlib import Path
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class cv:
    def __init__(self,pdf_path="",json_path="/CV") -> None:
        self.pdf_path=pdf_path
        self.json_path=json_path
        self.client=Client(host="http://192.168.0.165:11434")

    def extract_text_from_pdf(self):
        text= extract_text(self.pdf_path)
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\x00-\x7FéèàùçâêîôûëïüÿÉÈÀÙÇÂÊÎÔÛËÏÜŸ]+', ' ', text)
        return text
    async def toict(self):
        text=self.extract_text_from_pdf()  
        #"Text_CV":"",  
        prompt='Extract from the text datas in exactly this JSON Format: {"name": "","contact_number": "","email": "","Tools":[],"skills": [],"Profile_description": "","education_levels": [{"establishment":"","level" :""}],"Professional_experience":[{"establishment":"","job":"","Period in months":"","start_year":"","end_year":"","description": ""}],"Languages":[{"Language":","Level":""}],"Achievements":"","Job_recommanded":""}. if you do not find data let the field blank.Skills and tools must be a list of strings.in Text_CV dress textual description of the person using all data input.in Job_recommanded put a job description to recommande to the person according to his skills and experience.  Text:'
        #response = client.chat(model='llama3', messages=[
        #ollama.generate(model='llama3', prompt='Why is the sky blue?')
        print("Query LLM....")
        txt=""
        async for part in await AsyncClient(host="http://192.168.0.165:11434").chat(model='llama3', messages=[
            {
                'role': 'user',
                'content':f"{prompt},{text}"
                #'stream:': False,
                #'format':['json']
            }
        ], stream=True):
            #response=part['message']['content']
            print(part['message']['content'], end='', flush=True)
            txt=txt+part['message']['content']
        response=part
        print("End of query")
        text=response['message']['content']        
        b=txt.find('{')
        e=txt.rfind('}')+1
        dictt=txt[b:e]
        self.json_data= dictt
        return dictt
    def load_cv(self,json_file):
        if json_file.name.endswith(".json"):
            with open(json_file, "rb") as f:
                file_contents = f.read()
                json_data = json.loads(file_contents)
                return json_data
    def load_cv_dir(self,jobdescription):
        data=pd.DataFrame()
        persons=pd.DataFrame()
        skills=pd.DataFrame()
        Tools=pd.DataFrame()
        json_dir= Path("resources/data")
        for file in os.listdir(json_dir):
            if file.endswith('.json'):
                filename=os.path.join(json_dir,file)
                with open(filename, 'r') as f:
                    datafile = f.read()            
                    jsons = json.loads(datafile)
                    basic_info = pd.json_normalize(jsons)
                    data = pd.concat([data, basic_info], ignore_index=True)
        data['Tools']=data['Tools'].apply(lambda x: ','.join(x))
        data['email']=data['email'].apply(lambda x: ','.join(x) if isinstance(x,list) else x)
        data['skills']=data['skills'].apply(lambda x: ','.join(x))
        data['Languages']=data['Languages'].apply(json.dumps)
        data['education_levels']=data['education_levels'].apply(json.dumps)
        data['Professional_experience']=data['Professional_experience'].apply(json.dumps)
        selectedCol=['Tools','skills','Languages','education_levels','Professional_experience']
        data['profile'] = data[selectedCol].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
        texts =[jobdescription] +data['profile'].tolist()
        vectorizer = TfidfVectorizer().fit_transform(texts)
        vectors = vectorizer.toarray()
        cosine_similarities = cosine_similarity(vectors[0:1], vectors[1:])
        data['score']=cosine_similarities[0]
        return data
    
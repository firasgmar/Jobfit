from pdfminer.high_level import extract_text
import asyncio
from ollama import Client
from ollama import AsyncClient
import ollama
import json
import re
class cv:
    def __init__(self,pdf_path) -> None:
        self.pdf_path=pdf_path
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


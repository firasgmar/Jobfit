
import fitz
import re
from ollama import Client
class LLM_parser:
  def __init__(self):
    self.client = Client(host='http://10.21.220.15:11434')
  def query(self,messages):
    response = self.client.chat(model='llama3', messages=messages)
    return response['message']['content']
  def get_name(self,text):
    messages = [
        {"role": "system", "content": "Return the name of the person in CV data in this format  Name:  "},
        {"role": "user", "content": text}
    ]
    result = self.query(messages)
    return result
  def get_phone_number(self,text):
    messages = [
        {"role": "system", "content": "Return the phone number of the person in CV data in this format  phone number:  "},
        {"role": "user", "content": text}
    ]
    result = self.query(messages)
    return result
  def get_mail(self,text):
    messages = [
        {"role": "system", "content": "Return the mail of the person in CV data in this format  phone mail:  "},
        {"role": "user", "content": text}
    ]
    result = self.query(messages)
    return result
  def get_about(self,text):
    messages = [
        {"role": "system", "content": "generat a Summary profil  for the person in CV data,in this format  Summary:  "},
        {"role": "user", "content": text}
    ]
    result = self.query(messages)
    return result
  def get_hobbies(self,text):
    messages = [
        {"role": "system", "content": "get hobbies of the person in CV data,in this list format  Hobbies:[]  "},
        {"role": "user", "content": text}
    ]
    result = self.query(messages)
    return result
  def get_education(self,text):
    messages = [
        {"role": "system", "content": "get education degrees of the person in CV data,in this list format  Education:[]  "},
        {"role": "user", "content": text}
    ]
    result = self.query(messages)
    return result
  def get_experience(self,text):
    messages = [
        {"role": "system", "content": "get experiences  of the person in CV data,in this list format  experiences:[]  "},
        {"role": "user", "content": text}
    ]
    result = self.query(messages)
    return result
  def get_languages(self,text):
    messages = [
        {"role": "system", "content": "get languages  of the person in CV data,in this format  languages:[]  "},
        {"role": "user", "content": text}
    ]
    result = self.query(messages)
    return result
  def extract_text_from_pdf(self,pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text
  def clean_extracted_text(self,text):
      # Supprimer les espaces multiples
      text = re.sub(r'\s+', ' ', text)
      # Supprimer les nouvelles lignes multiples
      text = re.sub(r'\n+', '\n', text)
      return text
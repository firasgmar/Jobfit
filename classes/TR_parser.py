import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import fitz
import re
class TR_parser:
  def __init__(self):
    # Specify the LLM model we'll be using
    model_name = "Qwen/Qwen2-0.5B-Instruct"
    #model_name ="gpt2"
    # Configure for GPU usage
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map="auto",
        torch_dtype=torch.float16,
        trust_remote_code=True,
    )
    # Load the tokenizer for the chosen model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    # Create a pipeline object for easy text generation with the LLM
    self.pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)
    # Parameters to control LLM's response generation

  def query(self,messages):
    generation_args = {
        "max_new_tokens": 256,     # Maximum length of the response
        "return_full_text": False,      # Only return the generated text
    }
    """Sends a conversation history to the AI assistant and returns the answer.

    Args:
      messages (list): A list of dictionaries, each with "role" and "content" keys.

    Returns:
      str: The answer from the AI assistant.
    """

    output = self.pipe(messages, **generation_args)
    return output[0]['generated_text']
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
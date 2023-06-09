# -*- coding: utf-8 -*-
"""ABSTRACT SUMMARY EXPERIMENT.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IirSeAnkFecgUH1008RasVP45lW0Qyi7
"""

from google.colab import drive

drive.mount('/content/drive')

folder_path = "/content/drive/MyDrive/DFAS.csv"

import pandas as pd
from transformers import BartTokenizer, BartForConditionalGeneration
from tqdm import tqdm

model_name = 'facebook/bart-large-cnn'
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)

# Read the CSV file
data = pd.read_csv(folder_path)

# Create a new column for the summaries
data['Abstract Summary'] = ''

# Iterate through each row with a progress bar
for index, row in tqdm(data.head(100).iterrows(), total=len(data.head(100))):
    # Get the abstract from the 'Abstract' column
    abstract = row['Abstract']
    
    # Tokenize the abstract
    inputs = tokenizer.encode(abstract, return_tensors='pt', max_length=1024, truncation=True)
    
    # Generate the summary
    summary_ids = model.generate(inputs, num_beams=4, max_length=100, early_stopping=True)
    
    # Decode the summary tokens and convert to string
    summary = tokenizer.decode(summary_ids.squeeze(), skip_special_tokens=True)
    
    # Assign the summary to the 'Abstract Summary' column
    data.at[index, 'Abstract Summary'] = summary


NEW_path = "/content/drive/MyDrive/DFAS_V1.csv"


# Save the updated DataFrame to a new CSV file
with open(NEW_path, 'w', encoding = 'utf-8') as f:
  data.to_csv(f)

from transformers import PegasusForConditionalGeneration, PegasusTokenizer, AutoTokenizer
import torch

model2_name = "google/pegasus-xsum"
torch_device = 'cuda' if torch.cuda.is_available() else 'gpu'
tokenizer = AutoTokenizer.from_pretrained(model2_name)
model = PegasusForConditionalGeneration.from_pretrained(model2_name).to(torch_device)

def get_response(input_text):
  batch = tokenizer([input_text],truncation=True,padding='longest',max_length=1024, return_tensors="pt").to(torch_device)
  gen_out = model.generate(**batch,max_length=128,num_beams=5, num_return_sequences=1, temperature=1.5)
  output_text = tokenizer.batch_decode(gen_out, skip_special_tokens=True)
  return output_text

# Read the CSV file
data = pd.read_csv(folder_path)

# Create a new column for the summaries
data['Abstract Summary'] = ''

# Iterate through each row with a progress bar
for index, row in tqdm(data.head(100).iterrows(), total=len(data.head(100))):
    # Get the abstract from the 'Abstract' column
    abstract = row['Abstract']

    summary = get_response(abstract)

    data.at[index, 'Abstract Summary'] = summary

NEW_path = "/content/drive/MyDrive/DFAS_V2.csv"

# Save the updated DataFrame to a new CSV file
with open(NEW_path, 'w', encoding = 'utf-8') as f:
  data.to_csv(f)

pip install transformers

pip install transformers==4.29.1

import torch
from transformers import PegasusForConditionalGeneration, AutoTokenizer

model_name = "tuner007/pegasus_summarizer"
torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name).to(torch_device)

def get_response(input_text):
  batch = tokenizer([input_text],truncation=True,padding='longest',max_length=1024, return_tensors="pt").to(torch_device)
  gen_out = model.generate(**batch,max_length=128,num_beams=5, num_return_sequences=1, temperature=1.5)
  output_text = tokenizer.batch_decode(gen_out, skip_special_tokens=True)
  return output_text

# Read the CSV file
data = pd.read_csv(folder_path)

# Create a new column for the summaries
data['Abstract Summary'] = ''

# Iterate through each row with a progress bar
for index, row in tqdm(data.head(100).iterrows(), total=len(data.head(100))):
    # Get the abstract from the 'Abstract' column
    abstract = row['Abstract']

    summary = get_response(abstract)

    data.at[index, 'Abstract Summary'] = summary

NEW_path = "/content/drive/MyDrive/DFAS_V2.csv"

# Save the updated DataFrame to a new CSV file
with open(NEW_path, 'w', encoding = 'utf-8') as f:
  data.to_csv(f)

from transformers import T5ForConditionalGeneration, AutoTokenizer
import pandas as pd
from tqdm import tqdm

tokenizer4 = AutoTokenizer.from_pretrained("t5-small")
model4 = T5ForConditionalGeneration.from_pretrained("t5-small")

# Read the CSV file
data = pd.read_csv(folder_path)

# Create a new column for the summaries
data['Abstract Summary'] = ''

# Iterate through each row with a progress bar
for index, row in tqdm(data.head(100).iterrows(), total=len(data.head(100))):
    # Get the abstract from the 'Abstract' column
    abstract = row['Abstract']
    prefixed_abstract = ('summarize: ' + abstract)
    
    inputs = tokenizer4(prefixed_abstract, return_tensors="pt").input_ids
    summary_ids = model4.generate(inputs)
    summary = tokenizer4.decode(summary_ids[0], skip_special_tokens=True)

    data.at[index, 'Abstract Summary'] = summary

NEW_path = "/content/drive/MyDrive/DFAS_V4.csv"


# Save the updated DataFrame to a new CSV file
with open(NEW_path, 'w', encoding = 'utf-8') as f:
  data.to_csv(f)

from transformers import AutoModelForSeq2SeqLM

model5 = "snrspeaks/t5-one-line-summary"

model = AutoModelForSeq2SeqLM.from_pretrained(model5)
tokenizer = AutoTokenizer.from_pretrained(model5)

# Read the CSV file
data = pd.read_csv(folder_path)

# Create a new column for the summaries
data['Abstract Summary'] = ''

# Iterate through each row with a progress bar
for index, row in tqdm(data.head(100).iterrows(), total=len(data.head(100))):
    # Get the abstract from the 'Abstract' column
    abstract = row['Abstract']
    prefixed_abstract = ('summarize: ' + abstract)

    input_ids = tokenizer.encode("summarize: " + abstract, return_tensors="pt", add_special_tokens=True)
    generated_ids = model.generate(input_ids=input_ids,num_beams=5,max_length=50,repetition_penalty=2.5,length_penalty=1,early_stopping=True,num_return_sequences=3)
    preds = [tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=True) for g in generated_ids]


    data.at[index, 'Abstract Summary'] = preds

NEW_path = "/content/drive/MyDrive/DFAS_V5.csv"


# Save the updated DataFrame to a new CSV file
with open(NEW_path, 'w', encoding = 'utf-8') as f:
  data.to_csv(f)

import torch
from transformers import PegasusForConditionalGeneration, PegasusTokenizer, AutoTokenizer

model6_name = "google/pegasus-pubmed"
torch_device = 'cuda' if torch.cuda.is_available() else 'gpu'
tokenizer6 = AutoTokenizer.from_pretrained(model6_name, use_fast=False)
model6 = PegasusForConditionalGeneration.from_pretrained(model6_name).to(torch_device)

import torch
from transformers import PegasusForConditionalGeneration, PegasusTokenizer, AutoTokenizer

model6_name = "google/pegasus-pubmed"
torch_device = 'cuda' if torch.cuda.is_available() else 'gpu'
tokenizer6 = AutoTokenizer.from_pretrained(model6_name)
model6 = PegasusForConditionalGeneration.from_pretrained(model6_name).to(torch_device)
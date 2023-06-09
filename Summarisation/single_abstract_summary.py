# -*- coding: utf-8 -*-
"""Single Abstract Summary.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IZmbm5EHRlDJ_L4PJs5zZbmK7LoSUDLY
"""

pip install transformers==4.29.1

pip install sentencepiece

import torch
from transformers import PegasusForConditionalGeneration, AutoTokenizer

#Pegasus model fine-tuned on summarisation
model_name = "ArinaRomashova/summarisation-pegasus-pubmed"
torch_device = 'cuda' if torch.cuda.is_available() else 'gpu'

#Tokenizer and model instantiation
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name).to(torch_device)

#Summarisation function

def summarise (input_text):
  batch = tokenizer([input_text],truncation=True,padding='longest',max_length=1024, return_tensors="pt").to(torch_device)
  gen_out = model.generate(**batch,max_length=128,num_beams=5, num_return_sequences=1, temperature=1.5)
  output_text = tokenizer.batch_decode(gen_out, skip_special_tokens=True)
  return output_text

text = "The mobility support that guide dogs provide to the visually impaired person is one of the most established forms of assistive dog partnership. The UK has the highest number of guide dog owners per capita globally. While there exists a small body of literature on guide dog partnerships, very few studies have specifically addressed owners in the UK or examined partnerships as experienced by first-time owners. Little attention is paid to the professionals who work with guide dog-owner teams. This thesis explores the guide dog-person partnership as it is perceived by guide dog professionals and first-time owners in the UK. Two empirical studies are presented; data collection and analysis are guided by Interpretative Phenomenological Analysis. Study 1 examines the perspectives of five mobility specialists and dog trainers employed by Guide Dogs UK. Study 2 concerns 11 London-based first-time owners and their guide dog experience within and outside the contexts of joint mobility. The two studies foreground the ambivalence and fluidity that characterise the participants' perceptions of guide dog-person partnerships. The professionals' and owners' accounts depict the guide dogs taking up different and conflicting characters; they shift between being trustworthy guides and forces of dangerous unpredictability, between working animals and subjects of tender loving care. The person's role in the partnership can also take different forms, such as user, carer, 'manager,' and 'client.' The first-time owners' interviews shed further light on the guide dogs' impact on the existential level. The partnership helps re-establish the security and openness of the self's embodied relation with the physical world and re-embrace the possibility of a more home-like being within the sense of uncanny existence aggravated by sight loss. The owners' connections with their guide dogs also shape the social terrain through which their senses of self arise, in both welcome and unwelcome ways."

summarise(text)
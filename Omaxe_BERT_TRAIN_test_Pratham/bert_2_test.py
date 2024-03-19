import torch
from transformers import BertTokenizer, BertForSequenceClassification
import numpy as np
import json
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from sklearn.preprocessing import LabelEncoder
from tqdm import tqdm
from flask import Flask, render_template, request, jsonify
from langdetect import detect
from converter import hinglish_to_english
app = Flask(__name__)

with open('18_data.json') as file:
    data = json.load(file)

# Load fine-tuned BERT model and tokenizer
model_path = 'bert_final'  
tokenizer = BertTokenizer.from_pretrained(model_path)
model = BertForSequenceClassification.from_pretrained(model_path)
label_encoder = LabelEncoder()

def gen_response(question):

    # Detect the language of the input text
    detected_language = detect(question)
        
    if detected_language != 'en':
        question = hinglish_to_english(question)
        
    
    inputs = tokenizer(question, return_tensors="pt")
    input_ids = inputs["input_ids"]
    attention_mask = inputs["attention_mask"]

    # Classify input
    with torch.no_grad():
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)

    # Get predicted label
    
    predicted_label_idx = torch.argmax(outputs.logits).item()
    intents = [intent['tag'] for intent in data['intents']]

    # Initialize and fit LabelEncoder
    label_encoder = LabelEncoder()
    label_encoder.fit(intents)
    # print(predicted_label_idx,label_encoder.classes_.shape[0])
    if predicted_label_idx < len(label_encoder.classes_):
        # Perform inverse transformation if predicted label index is within range
        predicted_label = label_encoder.inverse_transform([predicted_label_idx])[0]
       
        
        for intent in data['intents']:
            if intent['tag'] == predicted_label:
                response = intent['responses']
                return response
           
    else:
            response = "Sorry, I can answer only questions relevant to Omaxe"
            return response



@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    return gen_response(msg)

if __name__ == '__main__':
    app.run()
    

import torch
from transformers import BertTokenizer, BertForSequenceClassification
import numpy as np
import json
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from sklearn.preprocessing import LabelEncoder
from tqdm import tqdm
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

with open('new.json') as file:
    data = json.load(file)

# Load fine-tuned BERT model and tokenizer
model_path = 'fine_tuned_bert_2'  # Adjust the path accordingly
tokenizer = BertTokenizer.from_pretrained(model_path)
model = BertForSequenceClassification.from_pretrained(model_path)
label_encoder = LabelEncoder()

# Sample input
# input_text = input("enter-> ")

# Tokenize input

# Find the intent from the JSON data
def gen_response(question):
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
    # print(label_encoder.classes_)
    predicted_label = label_encoder.classes_[predicted_label_idx] if predicted_label_idx < len(label_encoder.classes_) else "Unknown"
    # predicted_label = label_encoder.classes_[predicted_label_idx] if predicted_label_idx < len(label_encoder.classes_) else "Unknown"

    # Now you can use the label encoder for inverse transformation
    predicted_label = label_encoder.inverse_transform([predicted_label_idx])[0]

    response = "Sorry, I couldn't understand your question."
    for intent in data['intents']:
        if intent['tag'] == predicted_label:
            # Randomly select a response from the list of responses
            response = intent['responses']
            return response

# print("Input:", input_text)
# print("Predicted Intent:", predicted_label)
# print("Response:", response)


@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    return gen_response(msg)

if __name__ == '__main__':
    app.run()
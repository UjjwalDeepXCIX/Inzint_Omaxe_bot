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
from textblob import TextBlob
import requests
import base64

app = Flask(__name__)

with open('19_new.json') as file:
    data = json.load(file)

# Load fine-tuned BERT model and tokenizer
model_path = 'bert_4'  
tokenizer = BertTokenizer.from_pretrained(model_path)
model = BertForSequenceClassification.from_pretrained(model_path)
label_encoder = LabelEncoder()

def gen_response(question):
    
    # Detect the language of the input text
    detected_language = detect(question)
        
    if detected_language != 'en':
        question = hinglish_to_english(question)
    
    # Spell check the input question, excluding the keyword "Omaxe"
    spell_checked = []
    for word in question.split():
        if word.lower() == 'omaxe':
            spell_checked.append(word)
        else:
            spell_checked.append(TextBlob(word).correct().raw)
    question = ' '.join(spell_checked)
        
    question = TextBlob(question).correct().raw

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


# # Load unique words from words.json
# with open('words.json') as f:
#     unique_words = json.load(f)


# def gen_response(question):
#     # Tokenize the question
#     tokenized_question = question.split()
#     unique_word_found = False

#     for word in tokenized_question:
#         if word in unique_words:
#             unique_word_found = True
#             break

#     if unique_word_found:
#         # Your existing logic
#         # Detect the language of the input text
#         detected_language = detect(question)

#         if detected_language != 'en':
#             question = hinglish_to_english(question)

#         # Spell check the input question, excluding the keyword "Omaxe"
#         spell_checked = []
#         for word in tokenized_question:
#             if word.lower() == 'omaxe':
#                 spell_checked.append(word)
#             else:
#                 spell_checked.append(TextBlob(word).correct().raw)
#         question = ' '.join(spell_checked)

#         question = TextBlob(question).correct().raw

#         inputs = tokenizer(question, return_tensors="pt")
#         input_ids = inputs["input_ids"]
#         attention_mask = inputs["attention_mask"]

#         # Classify input
#         with torch.no_grad():
#             outputs = model(input_ids=input_ids, attention_mask=attention_mask)

#         # Get predicted label
#         predicted_label_idx = torch.argmax(outputs.logits).item()
#         intents = [intent['tag'] for intent in data['intents']]

#         # Initialize and fit LabelEncoder
#         label_encoder = LabelEncoder()
#         label_encoder.fit(intents)

#         if predicted_label_idx < len(label_encoder.classes_):
#             # Perform inverse transformation if predicted label index is within range
#             predicted_label = label_encoder.inverse_transform([predicted_label_idx])[0]

#             for intent in data['intents']:
#                 if intent['tag'] == predicted_label:
#                     response = intent['responses']
#                     return response
#         else:
#             response = "Sorry, I can answer only questions relevant to Omaxe"
#             return response
#     else:
#         return "Sorry, the question is not relevant."





# Predefined list of suggestesions

def load_suggestions_from_json(json_file_path):
    with open('suggestions.json', 'r') as file:
        suggestions = json.load(file)
    return suggestions

# Assuming predefined_suggestions is a list of suggestions loaded from the JSON file
predefined_suggestions = load_suggestions_from_json('suggestions.json')



@app.route('/suggest', methods=['POST'])
def suggest():
    input_text = request.form['input_text'].lower()
    suggestions = get_suggestions(input_text)
    return jsonify(suggestions)     


def get_suggestions(input_text):
    return [suggestion for suggestion in predefined_suggestions if input_text.lower() in suggestion.lower()]

@app.route("/")
def index():
    return render_template('chat.html')

@app.route('/save_and_send', methods=['GET', 'POST'])
def save_and_send():
    # # Get form data
    email = request.form['email']
    category = request.form['category']
    query = request.form['taskdescription']

    # Save data to database or perform any other necessary operations

    # Get form data
    # email = "test@gmail.com"
    # category = "any category from form"
    # query = "kuch to likha hi hoga"

    # Call function to send email
    send_email(email, category, query)

    

    return render_template('chat.html')


def send_email(email, category, query):
    # Get form data
    # subject = request.form['subject']
    subject = f'New query from {category} category'
    # sender_name = request.form['from_name']
    sender_name = "User"
    # sender_email = request.form['from']
    sender_email = email
    recipient_email = "bigsecxxv@gmail.com"
    # body = request.form['body']
    body = f'New query from {category} category: {query}'

    # Create the payload
    payload = {
        "sender": {
            "name": sender_name,
            "email": sender_email
        },
        "to": [
            {
                "email": recipient_email
            }
        ],
        "subject": subject,
        "htmlContent": body
    }

    # Handle file attachments
    if 'attachment' in request.files:
        attachment = request.files['attachment']
        if attachment.filename != '':
            attachment_filename = attachment.filename
            attachment_content = attachment.read()
            attachment_part = {
                "name": attachment_filename,
                "content": base64.b64encode(attachment_content).decode('utf-8')
            }
            payload["attachment"] = [attachment_part]

    # API server information
    api_key = "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"
    api_url = "https://api.sendinblue.com/v3/smtp/email"

    response = requests.post(api_url, headers={"api-key": api_key}, json=payload)
    if response:
        # Determine if scrolling is needed based on the route
        scroll_to_contact = True if request.path.endswith('/sent') else False

        return render_template("chat.html", status="Successfully", scroll_to_contact=scroll_to_contact)
    else:
        # If the response status code is not 200, you might want to handle the error case.
        # You can optionally include more details about the error in the return statement.
        # return f'Failed to send email. Status code: {response.status_code}, Response: {response.text}'
        # return render_template("index.html", status="Failed")
        # Determine if scrolling is needed based on the route
        scroll_to_contact = True if request.path.endswith('/sent') else False

        return render_template("chat.html", status="Successfully", scroll_to_contact=scroll_to_contact)

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    return gen_response(msg)




if __name__ == '__main__':
    app.run()
    



import json
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from tqdm import tqdm


from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from flask import Flask, render_template, request, jsonify
import random
import json

import numpy as np





# Load JSON data
with open('new.json') as file:
    data = json.load(file)


app = Flask(__name__)



# Extract patterns and corresponding intents
patterns = []
intents = []
for intent in data['intents']:
    for pattern in intent['patterns']:
        patterns.append(pattern)
        intents.append(intent['tag'])

# Encode intents
label_encoder = LabelEncoder()
encoded_intents = label_encoder.fit_transform(intents)

# Split data into training and validation sets
train_patterns, val_patterns, train_intents, val_intents = train_test_split(patterns, encoded_intents, test_size=0.2, random_state=42)

# Tokenize patterns
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
train_encodings = tokenizer(train_patterns, truncation=True, padding=True)
val_encodings = tokenizer(val_patterns, truncation=True, padding=True)

# Create dataset
class IntentDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

train_dataset = IntentDataset(train_encodings, train_intents)
val_dataset = IntentDataset(val_encodings, val_intents)

# Load pre-trained BERT model
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=len(set(intents)))

# Fine-tune the model
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
model.to(device)
model.train()
train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)

optim = torch.optim.AdamW(model.parameters(), lr=5e-5)
epochs = 3
for epoch in range(epochs):
    print(f"Epoch {epoch+1}/{epochs}")
    epoch_loss = 0
    for batch in tqdm(train_loader, desc=f"Training Epoch {epoch+1}/{epochs}"):
        optim.zero_grad()
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['labels'].to(device)
        outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss
        epoch_loss += loss.item()
        loss.backward()
        optim.step()
    print(f"Epoch {epoch+1} Loss: {epoch_loss/len(train_loader):.4f}")

# Evaluate the model
model.eval()
val_loader = DataLoader(val_dataset, batch_size=8, shuffle=False)
total_correct = 0
total_samples = 0
with torch.no_grad():
    for batch in tqdm(val_loader, desc="Validating"):
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['labels'].to(device)
        outputs = model(input_ids, attention_mask=attention_mask)
        predictions = torch.argmax(outputs.logits, dim=1)
        total_correct += (predictions == labels).sum().item()
        total_samples += labels.size(0)

accuracy = total_correct / total_samples
print(f'Validation accuracy: {accuracy:.4f}')

# app.py

def ask_question(question):
    encoded_question = tokenizer(question, truncation=True, padding=True, return_tensors="pt")
    outputs = model(**encoded_question)
    predicted_label = torch.argmax(outputs.logits[0]).item()
    predicted_intent = label_encoder.inverse_transform([predicted_label])[0]

    # Find the intent from the JSON data
    for intent in data['intents']:
        if intent['tag'] == predicted_intent:
            # Randomly select a response from the list of responses
            response = np.random.choice(intent['responses'])
            return response
        else:
            continue
    else:
        return "Sorry, I couldn't understand your question."
    


model.save_pretrained("fine_tuned_bert_2")
tokenizer.save_pretrained("fine_tuned_bert_2")  


@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    return ask_question(msg)

if __name__ == '__main__':
    app.run()



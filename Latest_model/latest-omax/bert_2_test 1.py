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



# Predefined list of suggestions
predefined_suggestions = [
    "Omaxe",
    "flag",
    "new",
    "Omaxe World Street",
    "Omaxe World Street in Sector 79 Faridabad",
    "Best Retail Project at the Estatesmen Awards 2021",
    "Themed high street destination",
    "Shopping destination in Faridabad",
    "What makes Omaxe World Street unique?",
    "Why choose Omaxe World Street?",
    "What is special about Omaxe World Street?",
    "Investing in Lucknow",
    "Best places to invest in Lucknow",
    "Where to invest in Lucknow",
    "Property investment in Lucknow",
    "Lucknow real estate opportunities",
    "Why invest in Lucknow?",
    "Real estate market in Lucknow",
    "Property trends in Lucknow",
    "Lucknow property prices",
    "Residential investment in Lucknow",
    "Commercial real estate in Lucknow",
    "Penthouse Destination in Chandigarh",
    "Best penthouses in Chandigarh",
    "Where to find penthouses in Chandigarh",
    "Luxury penthouses in Chandigarh",
    "OMAXE penthouses in Chandigarh",
    "Chandigarh real estate",
    "Penthouse living in Chandigarh",
    "Chandigarh urban design",
    "Chandigarh modern architecture",
    "Premium residences in Chandigarh",
    "Penthouse lifestyle in Chandigarh",
    "Chandigarh property trends",
    "Commercial Spaces in Delhi",
    "Office spaces in Delhi",
    "Commercial properties in Delhi",
    "Delhi retail market",
    "Capital commercial spaces",
    "Business spaces in Delhi",
    "Commercial real estate in Delhi",
    "Commercial hubs in Delhi",
    "Delhi commercial developments",
    "Commercial projects in Delhi",
    "Investing in Delhi commercial spaces",
    "Modular steel structure at Omaxe Chowk",
    "Game changer in real estate",
    "Construction technology at Omaxe Chowk",
    "Chandni Chowk redevelopment project",
    "Omaxe Chowk multi-level parking",
    "Parking solutions in Chandni Chowk",
    "Advanced construction methods",
    "Omaxe Chowk project details",
    "Jindal Steel and Power Ltd. partnership",
    "Chandni Chowk traffic alleviation",
    "Omaxe Chowk construction update",
    "Omaxe Residency II Lucknow",
    "Luxury apartments in Gomti Nagar Extension",
    "Real estate developments in Lucknow",
    "2bhk and 3bhk apartments in Lucknow",
    "Omaxe Residency II features and amenities",
    "Residential spaces in Gomti Nagar Extension",
    "Transformational lifestyle in Omaxe Residency II",
    "Omaxe Residency II project details",
    "Luxury living in Lucknow",
    "Real estate investments in Gomti Nagar Extension",
    "Best Time to Buy Your Dream Home in Lucknow",
    "Lucknow, the City of Tehzeeb",
    "Reasons to buy your dream home in Lucknow",
    "Lucknow is a great option when it comes to investing in real estate",
    "Real Estate Sector Trends In 2024",
    "Trends In 2024",
    "Real Estate Sector in 2024",
    "2024 Real Estate Trends",
    "Omaxe Chowk",
    "Omaxe Chowk Awards",
    "Multi-level parking cum commercial development project in Chandni Chowk",
    "Omaxe Chowk Features",
    "Chandni Chowk Redevelopment",
    "Omaxe Chowk Gateway to Chandni Chowk",
    "Real estate investment in India",
    "Is real estate a profitable investment?",
    "Property investment in India",
    "Investing in Indian real estate",
    "Real estate investment advice",
    "Is it the right time for property investment in India?",
    "Scope for real estate investment in India",
    "Real estate market analysis in India",
    "Benefits of investing in Indian real estate",
    "Considerations before buying commercial space",
    "Reasons to invest in New Chandigarh property market",
    "Independent houses for sale in Allahabad",
    "Looking for independent houses in Prayagraj",
    "Best time to buy 4 BHK apartments in Lucknow",
    "Investing in real estate in Lucknow",
    "Invest in Omaxe properties in Indore this Diwali",
    "Diwali investment in Omaxe Indore homes",
    "Looking for 3 BHK flats in Ludhiana",
    "Interested in buying 3 BHK apartments in Ludhiana",
    "Need information about 3 BHK flats for sale in Ludhiana",
    "Looking for 3 BHK flats in Ludhiana",
    "Interested in buying 3 BHK apartments in Ludhiana",
    "Need information about 3 BHK flats for sale in Ludhiana",
    "What is Omaxe Chowk\u00e2\u20ac\u2122s progress?",
    "How have you secured the funding for Omaxe Chowk?",
    "How do you intend to retire your debt?",
    "What are your plans for the residential segment going ahead?",
    "What is Covid\u00e2\u20ac\u2122s impact on retail?",
    "What future do you see for the office rentals business?",
    "Is there a growing demand for quality housing in tier II and III cities?",
    "Looking for office spaces in Faridabad?",
    "Interested in commercial properties in Faridabad?",
    "Seeking investment opportunities in Faridabad?",
    "Want to know about OMAXE Faridabad?",
    "Interested in real estate investment?",
    "Looking for investment opportunities?",
    "Considering buying properties?",
    "Want to know about the real estate sector?",
    "Interested in investing in India?",
    "Considering real estate investment in India?",
    "Exploring investment options for NRIs?",
    "Want to know about NRI investments?",
    "Considering a career in real estate?",
    "Interested in joining the real estate sector?",
    "Want to know about real estate career options?",
    "Exploring opportunities in the real estate industry?",
    "Interested in real estate investments with assured returns?",
    "Exploring options for assured returns in real estate?",
    "Considering investments with assured returns in Indian real estate?",
    "Want to know about real estate investments offering assured returns?",
    "Considering Omaxe for real estate investments?",
    "Exploring real estate investment opportunities with Omaxe?",
    "Looking for trusted real estate developers like Omaxe for investments?",
    "Interested in Omaxe's real estate projects for investment purposes?",
    "Interested in investing in penthouses?",
    "Exploring investment opportunities in penthouses?",
    "Considering penthouses for investment purposes?",
    "Want to know about investing in penthouse properties?",
    "Exploring penthouse options in New Chandigarh?",
    "Looking for penthouse properties in New Chandigarh?",
    "Interested in investing in penthouses in New Chandigarh?",
    "Considering Omaxe's penthouse projects in New Chandigarh?",
    "Interested in the Chandni Chowk redevelopment project?",
    "Exploring investment opportunities in Chandni Chowk redevelopment?",
    "Considering investments in Chandni Chowk's redevelopment?",
    "Want to know about investing in Chandni Chowk's redevelopment?",
    "Want to know about Omaxe's investment track record?",
    "Exploring Omaxe's performance in real estate investments?",
    "Considering Omaxe's track record for investment purposes?",
    "Interested in Omaxe's investment success stories?",
    "Interested in luxury living with Omaxe?",
    "Exploring upscale residential options with Omaxe?",
    "Looking for luxurious homes by Omaxe?",
    "Considering investments in commercial real estate?",
    "Exploring commercial property investment options?",
    "Interested in lucrative commercial real estate ventures?",
    "Curious about real estate trends in 2024?",
    "Exploring the future of real estate in 2024?",
    "What are the upcoming trends in the real estate industry?",
    "Searching for affordable housing options with Omaxe?",
    "Interested in budget-friendly homes by Omaxe?",
    "Exploring Omaxe's affordable housing projects?",
    "Looking for effective property investment strategies?",
    "Interested in smart property investment techniques?",
    "Exploring ways to maximize returns on property investments?",
    "Interested in sustainable real estate projects?",
    "Exploring eco-friendly property options?",
    "Looking for green real estate developments?",
    "Seeking insights into the real estate market in India?",
    "Interested in real estate market analysis reports?",
    "Exploring trends and forecasts in the Indian real estate market?",
    "Looking for dream property online during lockdown?",
    "Searching for properties online during lockdown?",
    "How to find dream property during lockdown?",
    "How to allocate budget for property investment?",
    "Determining budget for property investment?",
    "Setting budget for property purchase?",
    "What are the key considerations for property location?",
    "How to choose the right location for property purchase?",
    "Factors to consider when selecting property location?",
    "How to be a smart consumer during virtual property tours?",
    "Best practices for virtual property visits?",
    "Tips for virtual property tours?",
    "How to set alerts for property updates?",
    "Setting up alerts for preferred property listings?",
    "Getting notified about property updates?",
    "What is the impact of lockdown on the real estate industry?",
    "How has the lockdown affected property buying?",
    "Impact of COVID-19 on real estate market?",
    "What measures has the government taken to boost the real estate sector?",
    "Government initiatives for real estate development?",
    "Steps taken by the government to support property buyers?",
    "What is the status of real estate market in Delhi?",
    "How is Delhi's real estate market performing?",
    "Overview of Delhi's real estate sector?",
    "What are the investor-friendly policies in Delhi?",
    "How has the government supported real estate investment in Delhi?",
    "Government policies favoring real estate investment?",
    "What makes Delhi an attractive investment destination?",
    "How is the infrastructure in Delhi favorable for investment?",
    "Importance of infrastructure in Delhi for investors?",
    "Why is Delhi considered a large consumer market?",
    "What contributes to Delhi's status as a major consumer market?",
    "Factors driving Delhi's consumer market?",
    "What makes Delhi's workforce competitive?",
    "Why is Delhi known for its skilled workforce?",
    "Factors contributing to Delhi's competent workforce?",
    "What is Omaxe Chowk commercial space all about?",
    "Can you provide an overview of commercial space in Omaxe Chowk?",
    "Tell me about Omaxe Chowk's commercial property.",
    "What are the unique features of Omaxe Chowk commercial space?",
    "Can you list down the distinctive aspects of Omaxe Chowk's commercial property?",
    "What makes Omaxe Chowk commercial space stand out?",
    "What are the benefits of investing in Omaxe Chowk commercial space?",
    "Why should one consider investing in commercial space at Omaxe Chowk?",
    "What advantages does Omaxe Chowk's commercial property offer to investors?",
    "What is Chandni Chowk known for?",
    "Can you provide an overview of Chandni Chowk's streets?",
    "Tell me about the streets of Chandni Chowk.",
    "What can one expect while shopping in Chandni Chowk?",
    "Describe the shopping experience in Chandni Chowk.",
    "What makes shopping in Chandni Chowk unique?",
    "How will Omaxe Chowk impact Chandni Chowk?",
    "What changes will Omaxe Chowk bring to Chandni Chowk?",
    "Describe the significance of Omaxe Chowk in Chandni Chowk's development.",
    "What is Chandni Chowk known for?",
    "Can you provide an overview of Chandni Chowk's streets?",
    "Tell me about the streets of Chandni Chowk.",
    "What can one expect while shopping in Chandni Chowk?",
    "Describe the shopping experience in Chandni Chowk.",
    "What makes shopping in Chandni Chowk unique?",
    "How will Omaxe Chowk impact Chandni Chowk?",
    "What changes will Omaxe Chowk bring to Chandni Chowk?",
    "Describe the significance of Omaxe Chowk in Chandni Chowk's development.",
    "What is the history of Chandni Chowk?",
    "Can you tell me about the historical background of Chandni Chowk?",
    "Describe the origin of Chandni Chowk.",
    "How important is Omaxe Chowk for Chandni Chowk?",
    "What role does Omaxe Chowk play in the development of Chandni Chowk?",
    "Describe the significance of Omaxe Chowk in Chandni Chowk's landscape.",
    "What impact will Omaxe Chowk's development have on Chandni Chowk?",
    "How will the development of Omaxe Chowk affect Chandni Chowk?",
    "Describe the changes expected with the development of Omaxe Chowk.",
    "What is Omaxe Ananda's Ganga view offering?",
    "Tell me about the Ganga views from Omaxe Ananda.",
    "What does Omaxe offer in terms of Ganga views from homes?",
    "Where is Omaxe Ananda located?",
    "Tell me about the location and connectivity of Omaxe Ananda.",
    "What are the nearby attractions of Omaxe Ananda?",
    "What features does Omaxe Ananda offer?",
    "Tell me about the facilities at Omaxe Ananda.",
    "What are the amenities available at Omaxe Ananda?",
    "What is Omaxe Connaught Place (OCP) known for?",
    "Can you describe the features of Omaxe Connaught Place?",
    "What makes OCP stand out as a shopping destination?",
    "Where is Omaxe Connaught Place located?",
    "How accessible is OCP from Delhi and Greater Noida?",
    "What are the transportation options available to reach OCP?",
    "What sets Omaxe Connaught Place apart from other malls?",
    "Can you highlight some of the unique attractions of OCP?",
    "Why should someone visit OCP for shopping and entertainment?",
    "What is Omaxe Connaught Place (OCP) all about?",
    "Can you provide information about OCP - Omaxe Connaught Place?",
    "What makes Omaxe Connaught Place a unique mall in Delhi NCR?",
    "What are the key features of Omaxe Connaught Place?",
    "Can you list some attractions and facilities at OCP?",
    "What makes Omaxe Connaught Place stand out among other malls in Delhi NCR?",
    "What are the residential options available at The Lake, New Chandigarh?",
    "Can you describe the types of residences offered at The Lake?",
    "What are the housing options at Omaxe's The Lake in New Chandigarh?",
    "What are the key features of The Lake by Omaxe?",
    "Can you list some amenities and attractions at The Lake, New Chandigarh?",
    "What makes The Lake a desirable residential destination in Chandigarh?",
    "What historical sites can I explore in Lucknow City?",
    "Can you recommend some historical places to visit in Lucknow?",
    "Where can I find good food in New Lucknow?",
    "What are some popular eateries in New Lucknow?",
    "What is the nightlife like in Lucknow?",
    "Are there any pubs or bars in Lucknow?",
    "Where can I go shopping in Lucknow City?",
    "What are some popular shopping destinations in Lucknow?",
    "What entertainment options are available in Lucknow?",
    "Where can I watch a movie in Lucknow City?",
    "What activities can I do at Omaxe New Lucknow?",
    "What facilities are available at Omaxe New Lucknow?",
    "What is Omaxe's contribution to the real estate sector?",
    "Can you tell me about Omaxe's role in the real estate industry?",
    "In which states does Omaxe have a presence?",
    "Where does Omaxe operate its projects?",
    "Can you tell me about Omaxe's projects in Delhi-NCR?",
    "What are some prominent Omaxe projects in Delhi-NCR?",
    "What residential projects has Omaxe undertaken?",
    "Can you tell me about Omaxe's residential properties?",
    "Where else does Omaxe have a presence?",
    "What are some other states where Omaxe operates?",
    "What are the benefits of investing in Allahabad real estate?",
    "Can you tell me why I should invest in property in Allahabad?",
    "What is the infrastructure like in Allahabad?",
    "How is the connectivity in Allahabad?",
    "What are the lifestyle and cultural attractions in Allahabad?",
    "Can you tell me about the cultural heritage of Allahabad?",
    "Does Omaxe have projects in Allahabad?",
    "Can you tell me about Omaxe's presence in Allahabad?",
    "What is the importance of the real estate sector in Lucknow?",
    "Can you tell me about the significance of real estate in Lucknow?",
    "Does Omaxe have projects in Lucknow?",
    "Can you tell me about Omaxe's projects in Lucknow?",
    "What are the features of Omaxe Residency-II in Lucknow?",
    "Can you describe the amenities offered at Omaxe Residency-II?",
    "Does Omaxe have projects in Ludhiana?",
    "Can you tell me about Omaxe's projects in Ludhiana?",
    "What are the features of Omaxe Ludhiana?",
    "Can you describe the amenities offered at Omaxe Ludhiana?",
    "What is the significance of Ganga-Yamuna Sangam?",
    "Can you tell me about Ganga-Yamuna Sangam?",
    "Why is Prayagraj important?",
    "Can you tell me about the significance of Prayagraj?",
    "What are the places to visit in Prayagraj during Kumbh?",
    "Can you suggest some tourist spots in Prayagraj during Kumbh?",
    "Tell me about Omaxe properties in Prayagraj.",
    "Can you provide information about Omaxe properties in Prayagraj?",
    "What are some amazing places to visit in Prayagraj during Kumbh?",
    "Can you tell me about the must-visit places in Prayagraj during Kumbh?",
    "Why is Ludhiana City important?",
    "Can you tell me about the significance of Ludhiana City?",
    "3 BHK Flat In Lucknow",
    "3 bhk flat",
    "buy 3 bhk flat in Lucknow",
    "home in Lucknow",
    "buy home in Lucknow",
    "property for sale in Lucknow",
    "New Lucknow Property",
    "properties in New Lucknow",
    "buy property in New Lucknow",
    "Omaxe Residency-II",
    "buy apartment in Omaxe Residency-II",
    "property in Omaxe Residency-II",
    "property for sale in Lucknow",
    "buy property in Lucknow",
    "real estate for sale in Lucknow",
    "Property in Lucknow",
    "buy property in Lucknow",
    "real estate in Lucknow",
    "Luxury Living in Ludhiana",
    "high-end lifestyle Ludhiana",
    "Real Estate Investment",
    "property investment Ludhiana",
    "Modern Living Spaces",
    "contemporary homes Ludhiana",
    "Exclusive Penthouse Lifestyle",
    "luxurious living Ludhiana",
    "Elite Living Experience",
    "premium lifestyle Ludhiana",
    "High-End Residential Projects",
    "luxury residences Ludhiana",
    "Exclusive Amenities",
    "premium facilities Ludhiana",
    "Prime Location Advantage",
    "convenient location Ludhiana",
    "How to determine your budget before buying a 3-BHK flat?",
    "What factors should be considered while determining the budget for a flat purchase?",
    "Looking for tips on setting a budget for buying a 3-BHK flat?",
    "What are the key features and specifications to look for in a 3-BHK flat?",
    "Seeking modern amenities and features in a 3-BHK flat?",
    "Interested in knowing about the specifications of 3-BHK flats in Lucknow?",
    "How to determine the carpet area of a 3-BHK flat?",
    "What is the significance of the carpet area while buying a flat?",
    "Seeking clarity on the difference between built-up area and carpet area in flats?",
    "How important is the builder's track record while buying a 3-BHK flat?",
    "What should buyers consider regarding the builder's reputation?",
    "Seeking trustworthy builders for buying 3-BHK flats?",
    "who is director of omaxe",
    "tell me some properties in new chandigarh"
]



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
    

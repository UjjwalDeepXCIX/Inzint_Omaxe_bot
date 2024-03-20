from googletrans import Translator

def hinglish_to_english(text):
    translator = Translator(service_urls=[
      'translate.google.com',
      'translate.google.co.kr',
    ])
    translated_text = translator.translate(text, src='hi', dest='en').text
    return translated_text
eng = hinglish_to_english("weather")


print(eng)
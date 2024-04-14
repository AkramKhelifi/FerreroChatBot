import re

def preprocess_input(input_sentence):
    sentence = input_sentence.lower()
    sentence = re.sub(r'[^a-z0-9\s]', '', sentence)
    sentence = re.sub(r'\s+', ' ', sentence).strip()
    return sentence
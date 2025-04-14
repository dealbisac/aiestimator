from langdetect import detect
from deep_translator import GoogleTranslator

def detect_language(text):
    return detect(text)

def translate_text(text, target):
    return GoogleTranslator(source="auto", target=target).translate(text)

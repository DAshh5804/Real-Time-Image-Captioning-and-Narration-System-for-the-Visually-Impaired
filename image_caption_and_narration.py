import tempfile
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from googletrans import Translator
from gtts import gTTS
import pygame

# Initialize model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

# Initialize audio playback
pygame.mixer.init()

target_language = 'en'  # Set your target language

def translate_text(text):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text

def speak_gtts(text):
    audio_file = tempfile.mktemp(suffix='.mp3')
    tts = gTTS(text=text, lang=target_language)
    tts.save(audio_file)
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def generate_caption(image_path):
    image = Image.open(image_path)
    inputs = processor(images=image, return_tensors="pt")
    outputs = model.generate(**inputs)
    caption = processor.decode(outputs[0], skip_special_tokens=True)
    
    filtered_caption = ' '.join(word for word in caption.split() if not word.lower().startswith('araf'))
    
    translated_caption = translate_text(filtered_caption)
    return translated_caption

def get_translated_message(caption):
    base_message = "You have been sent an image: "
    translated_base = translate_text(base_message)
    return f"{translated_base} {caption}"

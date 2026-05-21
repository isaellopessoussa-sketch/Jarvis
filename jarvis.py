import google.generativeai as genai
import speech_recognition as sr
from gtts import gTTS
import os

# 1. Configure sua chave do Google AI Studio aqui
GENAI_API_KEY = "AIzaSyAQke8gkGvLJBuWYDZMinLF4FVexEfSaRQ"
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def ouvir():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ouvindo...")
        audio = r.listen(source)
    try:
        texto = r.recognize_google(audio, language='pt-BR')
        print(f"Você disse: {texto}")
        return texto
    except:
        return ""

def falar(texto_resposta):
    tts = gTTS(text=texto_resposta, lang='pt')
    tts.save("resposta.mp3")
    # Comando para reproduzir áudio no ambiente Linux do Codespaces
    os.system("play resposta.mp3") 

print("J.A.R.V.I.S. Iniciado!")
while True:
    comando = ouvir()
    if comando:
        # O Gemini processa o comando de forma inteligente
        resposta = model.generate_content(comando)
        print(f"Jarvis: {resposta.text}")
        falar(resposta.text)

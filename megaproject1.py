import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import pyautogui
from openai import OpenAI
import pytesseract
from PIL import Image

recognizer = sr.Recognizer()
engine = pyttsx3.init() 

def speak(text):
    engine.say(text)
    engine.runAndWait()

def aiProcess(command):
    client = OpenAI(api_key= "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",
    )

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
        {"role": "user", "content": command}
    ]
    )

    return completion.choices[0].message.content

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():
        webbrowser.open("https://www.ndtv.com/latest")

    elif"screenshot" in c.lower():
        pyautogui.screenshot("screenshot.png")
        speak("Screenshot taken.")

    elif "read image" in c.lower():
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Users\garim\AppData\Local\Programs\Tesseract-OCR'
        pytesseract.pytesseract.tesseract_cmd = r'C:\Users\garim\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'


    image_path =r"C:\Users\garim\OneDrive\Pictures\Screenshots\Screenshot 2024-12-05 153742.png"  # Or take latest screenshot or image file

    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        speak("Reading the document.")
        print(text)
        speak(text)
    except Exception as e:
        speak("Sorry, I could not read the image.")
        print(f"OCR error: {e}")

    else:
        # Let OpenAI handle the request
        output = aiProcess(c)
        speak(output) 




if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        # Listen for the wake word "Jarvis"
        # obtain audio from the microphone
        r = sr.Recognizer()
         
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
            word = r.recognize_google(audio)
            print("you said : " , word)
            if(word.lower() == "jarvis"):
                speak("Ya")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    print("Recognized command :",command)

                    processCommand(command)


        except Exception as e:
            print("Error; {0}".format(e))



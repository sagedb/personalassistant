import speech_recognition as sr

# create recognizer and mic instances
recognizer = sr.Recognizer()
microphone = sr.Microphone()

with microphone as source:
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source)
print("Say something")
print("Did you say: " + recognizer.recognize_google(audio))
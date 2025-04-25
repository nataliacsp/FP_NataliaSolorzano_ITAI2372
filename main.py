import datetime
import speech_recognition as sr
import pyttsx3
import wikipedia
from textblob import TextBlob
from transformers import pipeline
from PIL import Image

def show_asa_avatar():
    img = Image.open("assets/asa_avatar.png")
    img.show()

# Speech setup
recognizer = sr.Recognizer()
engine = pyttsx3.init()
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

import json
import os

def load_profile():
    with open("asa_profile.json", "r") as file:
        profile = json.load(file)
    return profile


def login():
    asa_profile = load_profile()
    speak(f"My name is {asa_profile['name']}, short for {asa_profile['full_name']}.")
    speak(f"I’m a {asa_profile['color']} robot with a {asa_profile['look']}.")

    if not os.path.exists("users.json"):
        speak("User login system not found.")
        exit()

    with open("users.json", "r") as f:
        users = json.load(f)

    speak("Please enter your crew ID.")
    username = input("👩‍🚀 Username: ").strip().lower()

    if username not in users:
        speak("Crew ID not recognized.")
        exit()

    speak("Enter your password.")
    password = input("🔑 Password: ").strip()

    if users[username]["password"] == password:
        speak(f"Welcome aboard, Commander {username.capitalize()}.")
        return username
    else:
        speak("Password incorrect.")
        exit()



def speak(text):
    print("💬 ASA says:", text)
    engine.say(text)
    engine.runAndWait()


show_asa_avatar()


def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("🎙️ Listening...")
        audio = recognizer.listen(source, phrase_time_limit=6)
    try:
        print("✅ Got it! Recognizing...")
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I didn't catch that."

def process_command(command, user):
    command = command.lower()

    if "your name" in command:
        speak("My name is ASA, cute and short for Astronaut Support Agent.")
    elif "joke" in command:
        speak("Why did the robot go on a diet? Because he had too many bytes.")
    elif "hello" in command or "hi" in command:
        speak("Hello there! How can I help you today?")
    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}.")
    elif "date" in command:
        current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today is {current_date}.")
    elif "weather" in command:
        speak("I can't check the weather yet, but I'm learning to do that soon.")
    elif "stop" in command or "goodbye" in command or "bye" in command:
        speak("Bye! ASA is shutting down now, until next time.")
        exit()
    elif "search" in command and "wikipedia" in command:
        topic = command.replace("search wikipedia for", "").strip()
        try:
            summary = wikipedia.summary(topic, sentences=2)
            speak(summary)
        except wikipedia.exceptions.DisambiguationError:
            speak("That topic is too broad. Try being more specific.")
        except wikipedia.exceptions.PageError:
            speak("I couldn’t find anything about that.")
    elif "start journal log" in command:
        speak("Starting Journal Log now. Create mode, edit mode, or read mode?")
        mode = listen().lower()

        if "create" in mode:
            speak("Date and time of entry, please.")
            entry_time = listen().strip()

            speak("Alright. I'm ready to log your thoughts.")
            journal_entry = listen()

            # Analyze sentiment
            blob = TextBlob(journal_entry)
            mood = blob.sentiment.polarity
            mood_tag = (
                "Positive" if mood > 0.2
                else "Negative" if mood < -0.2
                else "Neutral"
            )

            # Summarize journal entry
            try:
                summary_result = summarizer(journal_entry, max_length=50, min_length=15, do_sample=False)
                summary = summary_result[0]["summary_text"]
            except:
                summary = "Summary not available."

            user_folder = f"journal_logs/{user}"
            os.makedirs(user_folder, exist_ok=True)

            filename = f"{user_folder}/log_{entry_time.replace(' ', '_').replace(':', '-')}.txt"
            with open(filename, "w") as file:
                file.write(f"🕒 Entry Time: {entry_time}\n")
                file.write(f"😊 Mood: {mood_tag}\n")
                file.write("📝 Entry:\n")
                file.write(journal_entry + "\n")
                file.write(f"\n📋 Summary:\n{summary}")


            speak("Journal entry saved with summary and mood.")

        elif "read" in mode:
            speak("Which entry date and time would you like to hear?")
            requested_time = listen().strip()
            user_folder = f"journal_logs/{user}"
            filename = f"{user_folder}/log_{requested_time.replace(' ', '_').replace(':', '-')}.txt"

            try:
                with open(filename, "r") as file:
                    content = file.read()
                    speak("Reading your journal entry now.")
                    print("\n" + content)
                    speak(content)
            except FileNotFoundError:
                speak("I couldn't find a journal entry with that date and time.")

        elif "edit" in mode:
            speak("Edit mode is not available on this tier. You are currently using ASA Lite.")
            speak("To unlock advanced features like journal editing, mood trend analysis, and interstellar syncing, please upgrade to ASA Pro.")
            speak("Just kidding. I'm still learning how to edit entries. Stay tuned!")

    else:
        # Sentiment-based response
        blob = TextBlob(command)
        polarity = blob.sentiment.polarity

        if polarity > 0.2:
            speak("That sounds positive! I'm glad.")
        elif polarity < -0.2:
            speak("That sounds a bit negative. I'm here if you want to talk more.")
        else:
            speak("Hmm... I'm not sure how to respond to that yet. But I'm learning!")

# Main loop
try:
    print("🌟 ASA is waking up... Hello from your AI Semantic Agent!")
    current_user = login()  # << Call the login function first

    while True:
        command = listen()
        print("🧠 You said:", command)

        if "sorry" in command.lower():
            continue  # skip processing if ASA didn't catch anything

        process_command(command, current_user)

except KeyboardInterrupt:
    print("\n🌙 ASA shutting down. Talk to you soon!")


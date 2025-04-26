#CODE BY NATALIA SOLORZANO W207818526 
import time
import datetime
import speech_recognition as sr
import pyttsx3
import difflib
import wikipedia
from textblob import TextBlob
from transformers import pipeline
from PIL import Image
import json
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
from getpass import getpass



def speak(text):
    print("💬 ASA says:", text)
    engine.say(text)
    engine.runAndWait()
    time.sleep(0.8)

def show_asa_avatar():
    try:
        img = Image.open("assets/asa_avatar.png")
        img.show()
        speak("Here I am! This is my avatar: lilac-colored, bow-wearing, and lab coat-ready for space missions.")
    except FileNotFoundError:
        speak("Oops! I can't find my avatar image.")

recognizer = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")


VOICE_PROFILES = {
    "friendly": 1,    
    "calm": 2,        
    "professional": 3, 
    "robotic": 4      
}

def listen(timeout=30, phrase_time_limit=50):
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print(f"🎙️ Listening...")
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            print("✅ Got it! Recognizing...")
            return recognizer.recognize_google(audio)
        except sr.WaitTimeoutError:
            return "timeout"
        except sr.UnknownValueError:
            return "Sorry, I didn't catch that."


    
#def choose_voice():
    #speak("Commander, would you like me to use a friendly, calm, professional, or robotic voice today?")
   # choice = listen().lower()

   # for mood, index in VOICE_PROFILES.items():
        #if mood in choice:
            #engine.setProperty('voice', voices[index].id)
           #speak(f"Setting voice to {mood} mode.")
           # return

   # speak("No change made. I will continue using my default voice.")

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
    password = getpass("🔑 Password: ").strip()

    if users[username]["password"] == password:
        speak(f"Welcome aboard, Commander {username.capitalize()}.")
        return username
    else:
        speak("Password incorrect.")
        exit()

def listen_journal():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("🎙️ Listening for journal entry (long session)...")
        try:
            audio = recognizer.listen(source, timeout=180)  # Only timeout, no phrase_time_limit
            print("✅ Got it! Recognizing...")
            transcript = recognizer.recognize_google(audio).lower()

            if "end journal entry" in transcript or "exit journal log" in transcript:
                speak("Ending journal entry as requested.")
                return "exit_journal"

            return transcript

        except sr.WaitTimeoutError:
            speak("I didn’t hear anything for a while. Would you like to end this journal entry? Just say yes or no.")
            choice = listen(timeout=30, phrase_time_limit=30).lower()

            if "yes" in choice:
                return "exit_journal"
            elif "no" in choice:
                speak("Would you like to start over or continue where you left off?")
                follow_up = listen(timeout=30, phrase_time_limit=30).lower()

                if "start over" in follow_up:
                    speak("Okay. Starting over from the beginning.")
                    return "restart"
                elif "continue" in follow_up:
                    speak("Would you like me to read the last couple of sentences or continue recording?")
                    next_step = listen(timeout=30, phrase_time_limit=30).lower()

                    if "read" in next_step:
                        speak("Reading the last few sentences so you can pick up from where you left off.")
                        return "read_back"
                    else:
                        speak("Continuing your journal entry now.")
                        return "continue"
            return "timeout"
        except sr.UnknownValueError:
            return "Sorry, I didn't catch that."


def get_last_sentences(text, num_sentences=2):
    sentences = text.strip().split(".")
    last = ". ".join(sentences[-num_sentences:]).strip()
    return last + "." if last and not last.endswith(".") else last

def save_journal(user, mood_tag, entry_time, journal_entry, summary):
    now = datetime.datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%B")
    day = now.strftime("%d")

    # Build dynamic folder path
    user_folder = os.path.join("journal_logs", user, year, month, day)
    os.makedirs(user_folder, exist_ok=True)

    # Format filename: mood_log<entry_number>_<hour-minuteAMPM>.txt
    timestamp = now.strftime("%I-%M%p").lower()
    filename = f"{mood_tag.lower()}_log_{timestamp}.txt"
    file_path = os.path.join(user_folder, filename)

    with open(file_path, "w") as file:
        file.write(f"🕒 Entry Time: {entry_time}\n")
        file.write(f"😊 Mood: {mood_tag}\n")
        file.write("📝 Entry:\n")
        file.write(journal_entry + "\n")
        file.write(f"\n📋 Summary:\n{summary}\n")

    speak(f"Journal entry saved under {month} {day}, {year}. Mood: {mood_tag}.")


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
        print("🎧 ASA heard mode as:", mode)

        if "create" in mode or "new" in mode or "entry" in mode:
            speak("Date and time of entry, please.")
            entry_time = listen().strip()

            speak("Alright. I'm ready to log your thoughts.")
            journal_entry = listen_journal()

            if journal_entry == "exit_journal":
                speak("Journal entry session ended.")
                return

            elif journal_entry == "restart":
                speak("Please begin again when you're ready.")
                journal_entry = listen_journal()

            elif journal_entry == "read_back":
                last_part = get_last_sentences(journal_entry)
                speak("Here’s the last part of your entry so far:")
                speak(last_part)
                journal_entry = listen_journal()

            elif journal_entry == "continue":
                speak("Resuming recording now.")
                journal_entry = listen_journal()

            elif journal_entry == "timeout":
                speak("No input received. Exiting journal entry mode.")
                return

            if not isinstance(journal_entry, str):
                speak("I couldn’t process your journal. Please try again.")
                return

            if len(journal_entry.split()) < 30:
                summary = "Summary not generated — journal entry too short."
            else:
                try:
                    summary_result = summarizer(journal_entry, max_length=50, min_length=15, do_sample=False)
                    summary = summary_result[0]["summary_text"]
                except:
                    summary = "Summary not available."
                    
            blob = TextBlob(journal_entry)
            mood = blob.sentiment.polarity
            mood_tag = (
                "Positive" if mood > 0.2
                else "Negative" if mood < -0.2
                else "Neutral"
            )
            save_journal(user, mood_tag, entry_time, journal_entry, summary)

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
        blob = TextBlob(command)
        polarity = blob.sentiment.polarity

        if polarity > 0.2:
            speak("That sounds positive! I'm glad.")
        elif polarity < -0.2:
            speak("That sounds a bit negative. I'm here if you want to talk more.")
        else:
            speak("Hmm... I'm not sure how to respond to that yet. But I'm learning!")



# Main loop
WAKE_WORDS = ["wake up asa", "hey asa", "hi asa", "wake up agent", "hey agent", "hi agent"]
VOICE_USERS = {
    "natalia": "apple",
    "assem": "lunar",
    "max": "puppy"
}

try:
    print("🌟 ASA is sleeping... Say a wake word to activate her.")
    show_asa_avatar()
    #choose_voice()
    current_user = None

    #while True:
        
        #command = listen(timeout=10, phrase_time_limit=10)
        
        #if command == "timeout" or command == "Sorry, I didn't catch that.":
           # continue

        #print("🧠 You said:", command.lower())

        #if any(wake in command.lower() for wake in WAKE_WORDS):
            #speak("I'm awake, Commander. Who's there? Please state your crew ID.")
            #username_command = listen(timeout=30, phrase_time_limit=30).lower()

            #if username_command == "sorry, i didn't catch that." or username_command == "timeout":
                #speak("I didn't catch that. Please state your crew ID again.")
                #username_command = listen(timeout=30, phrase_time_limit=30).lower()

            #speak("Now, please state your access password.")
            #password_command = listen(timeout=30, phrase_time_limit=30).lower()

            #if password_command == "sorry, i didn't catch that." or password_command == "timeout":
                #speak("I didn't catch that. Please state your password again.")
                #password_command = listen(timeout=30, phrase_time_limit=30).lower()

            #print("🗝️ Voice Login Attempt:", username_command, "/", password_command)

            #success = False

            #for user, password in VOICE_USERS.items():
                #if user in username_command:
                    #similarity = difflib.SequenceMatcher(None, password, password_command).ratio()
                    #if similarity > 0.6:
                        #speak(f"Welcome aboard, Commander {user.capitalize()}.")
                        #current_user = user
                        #success = True
                        #break
                    #else:
                        #speak("Crew ID recognized. But password mismatch.")
                        #success = False
                        #break

            #if not success:
                #speak("Voice login failed. Please type your credentials manually.")
                #current_user = login()

            #break



    while True:
        command = listen(timeout=30, phrase_time_limit=50)
        print("🧠 You said:", command)

        if "sorry" in command.lower():
            continue

        process_command(command, current_user)

except KeyboardInterrupt:
    print("\n🌙 ASA shutting down. Talk to you soon!")



# ASA – Astronaut Support Agent 👩‍🚀🤖

ASA is a voice-activated, emotionally-aware AI assistant designed for astronauts during space missions. Built in Python with natural language processing and sentiment analysis, ASA helps crew members log journal entries, access information, and stay emotionally connected—all through speech.

## 🌟 Features

- 🎙 Voice recognition and command processing
- 🧠 Sentiment analysis with TextBlob
- 🤖 Transformer-powered summarization (HuggingFace `distilbart`)
- 🔐 Multi-user login system
- 📝 Per-user journal logging with timestamps and mood tags
- 📚 Voice-based Wikipedia search
- 🎨 Personality system (`asa_profile.json`)
- 🖼 Avatar display using Pillow (PIL)
- 💬 Fun ASA personality with ASA Lite/Pro tier joke
- 💻 Modular code structure for easy expansion

## 🖼 ASA Avatar

Upon startup, ASA displays her official visual identity using Pillow (PIL).
This avatar reflects her profile as a friendly, lilac-colored robot with a bow and a NASA lab coat—built to be a charming and mission-ready companion.

## 🧪 Tech Stack

- Python 3.10+
- `speech_recognition`
- `pyttsx3`
- `textblob`
- `transformers`
- `Pillow`
- `wikipedia`
- JSON for data handling

## 📁 Project Structure

```
/FP_NataliaSolorzano_ITAI2372/
├── main.py
├── users.json
├── asa_profile.json
├── requirements.txt
├── /journal_logs/
│   └── <user>/
│       └── log_*.txt
├── /assets/
│   └── asa_avatar.png
```

## 🚀 How to Run

1. Create and activate a virtual environment
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the assistant:
   ```
   python main.py
   ```

## 🔐 Default Users

Edit `users.json` to manage crew access:
```json
{
  "natalia": { "password": "orion1" },
  "assem": { "password": "lunar" },
  "max": { "password": "puppy" }
}
```

## 🪩 Bonus Features

- Personality-driven responses
- Avatar with spoken identity
- Future plans for GUI (Tkinter/Streamlit)
- Hugging Face web integration (planned)
- ASA Pro Edition coming soon 😉

## 👩‍💻 Created by

**Natalia Solorzano**  
For the NASA AI Agent 2025  
ITAI 2372 - AI Applications  

# test.py
import speech_recognition as sr
from gtts import gTTS
import os
from deep_translator import GoogleTranslator

def listen_and_translate(source_lang, target_lang):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("🎤 Speak now...")
        recognizer.adjust_for_ambient_noise(source)  # Reduce background noise
        audio = recognizer.listen(source)

    try:
        # Speech-to-Text
        text = recognizer.recognize_google(audio, language=source_lang)
        print(f"📝 Recognized: {text}")

        # Translation
        translated = GoogleTranslator(source=source_lang, target=target_lang).translate(text)
        print(f"🌍 Translated ({source_lang} ➝ {target_lang}): {translated}")

        # Text-to-Speech
        tts = gTTS(text=translated, lang=target_lang)
        tts.save("output.mp3")

        # Play the audio file
        if os.name == "nt":  # Windows
            os.system("start output.mp3")
        elif os.name == "posix":  # macOS/Linux
            os.system("afplay output.mp3" if "darwin" in os.sys.platform else "mpg123 output.mp3")

    except sr.UnknownValueError:
        print("⚠ Could not understand audio")
    except sr.RequestError:
        print("⚠ Speech recognition service unavailable")
    except Exception as e:
        print("⚠ Error:", e)

if __name__ == "__main__":
    src = input("Enter source language code (e.g., en, hi, ta): ").strip()
    tgt = input("Enter target language code (e.g., en, hi, ta): ").strip()
    listen_and_translate(src, tgt)

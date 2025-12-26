from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.ttk import Combobox

import speech_recognition as sr
from pydub import AudioSegment
import PyPDF2
import pyttsx3
import os
import tempfile

from deep_translator import GoogleTranslator
import winsound
import datetime
from gtts import gTTS
from playsound import playsound
import threading
import sys

sys.stdout.reconfigure(encoding='utf-8')
engine = pyttsx3.init()
# colors
root = tk.Tk()
root.geometry("1000x600")
root.configure(bg='#84a1e6')

#  icon 

icon_path = r"C:\Users\kerup\OneDrive\Desktop\kiki\python\tkinter dashboard\Images\icon.png"

image_icon = tk.PhotoImage(file=icon_path)

# IMPORTANT: keep a reference
root.iconphoto(False, image_icon)

#top frame

top_frame=Frame(root,bg='#161d3f',width=1000,height=130).place(x=1,y=0)

logo_path = r"C:\Users\kerup\OneDrive\Desktop\kiki\python\tkinter dashboard\Images\logo.png"
logo_icon = tk.PhotoImage(file=logo_path)
Label(top_frame,image=logo_icon,bg='#161d3f').place(x=40,y=20)
Label(top_frame,text="Text Tool", font='arial 20 bold',bg='#161d3f',fg='#fff').place(x=190 , y=40)

#text area

# Get supported languages
# Translator instance

# Text areas
text_area = Text(root, font='Roboto 14', bg='#cbe7c2', wrap=WORD)
text_area.place(x=40, y=140, width=600, height=200)

text_area1 = Text(root, font='Roboto 14', bg='#dddaf5', wrap=WORD)
text_area1.place(x=40, y=360, width=600, height=200)

# Get supported languages
languages_dict = GoogleTranslator().get_supported_languages(as_dict=True)
language_names = list(languages_dict.keys())  # english, tamil, hindi...

# Comboboxes
combo = ttk.Combobox(root, values=language_names, state='readonly', width=15)
combo.place(x=200, y=100)
combo.set("english")

combo1 = ttk.Combobox(root, values=language_names, state='readonly', width=15)
combo1.place(x=350, y=100)
combo1.set("tamil")

# Translate function
def translate_text():
    text = text_area.get("1.0", END).strip()

    if not text:
        messagebox.showwarning("Warning", "Please enter or upload text")
        return

    try:
        src_lang = languages_dict[combo.get()]
        tgt_lang = languages_dict[combo1.get()]

        translated = GoogleTranslator(
            source=src_lang,
            target=tgt_lang
        ).translate(text)

        text_area1.delete("1.0", END)
        text_area1.insert(END, translated)

    except Exception as e:
        messagebox.showerror("Error", str(e))


# Translator button
trans_icon = r'C:\Users\kerup\OneDrive\Desktop\kiki\python\tkinter dashboard\Images\trans.png'
image_icon4 = tk.PhotoImage(file=trans_icon)

trans = Button(root,image=image_icon4,compound=LEFT,bg='#161d3f',bd=0,command=translate_text)
trans.place(x=550, y=57)

# IMPORTANT: keep reference
trans.image = image_icon4


# ---------------- VOICE + SPEED LABELS ----------------
Label(root, text='Voice', font='arial 15 bold', bg='#84a1e6', fg='white')\
    .place(x=700, y=200)
Label(root, text='Speed', font='arial 15 bold', bg='#84a1e6', fg='white')\
    .place(x=700, y=250)

gender_combobox = ttk.Combobox(root,values=['Male', 'Female'],font='arial 14',state='readonly',width=10)
gender_combobox.place(x=800, y=200)
gender_combobox.set('Male')

# ---------------- SPEED SLIDER ----------------
current_value = tk.DoubleVar(value=160)

def slider_changed(value):
    value_label.config(text=str(int(float(value))))

slider = ttk.Scale(root,from_=80,to=250,orient='horizontal',command=slider_changed,variable=current_value)
slider.place(x=800, y=250)

value_label = ttk.Label(root, text="160")
value_label.place(x=905, y=255)

# ---------------- SPEAK FUNCTION ----------------
def speak_text():
    text = text_area1.get("1.0", END).strip()
    if not text:
        text = text_area.get("1.0", END).strip()
    if not text:
        return

    voices = engine.getProperty('voices')
    if gender_combobox.get() == 'Male':
        engine.setProperty('voice', voices[0].id)
    else:
        engine.setProperty('voice', voices[1].id)

    engine.setProperty('rate', int(current_value.get()))

    engine.say(text)
    engine.runAndWait()

# ---------------- SPEAK BUTTON ----------------
speak_path = r'C:\Users\kerup\OneDrive\Desktop\kiki\python\tkinter dashboard\Images\speak.png'
image_icon = tk.PhotoImage(file=speak_path)

speak = Button(root,image=image_icon,compound=LEFT,bg='#84a1e6',width=130,command=speak_text)
speak.place(x=700, y=380)


def get_downloads_path():
    return os.path.join(os.path.expanduser("~"), "Downloads")

def download_audio():
    text = text_area1.get("1.0", END).strip()
    if not text:
        return

    # Voice
    voices = engine.getProperty('voices')
    engine.setProperty(
        'voice',
        voices[0].id if gender_combobox.get() == 'Male' else voices[1].id
    )

    # Speed
    engine.setProperty('rate', int(current_value.get()))

    downloads = os.path.join(os.path.expanduser("~"), "Downloads")
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(downloads, f"translated_audio_{timestamp}.wav")

    # Save WAV
    engine.save_to_file(text, file_path)
    engine.runAndWait()   # 🔴 REQUIRED

    # ▶ PLAY WAV
    winsound.PlaySound(file_path, winsound.SND_FILENAME)

    print("Audio saved and played:", file_path)




speak_path1 = r'C:\Users\kerup\OneDrive\Desktop\kiki\python\tkinter dashboard\Images\download.png'
image_icon1 = tk.PhotoImage(file=speak_path1)

btn = Button(root,image=image_icon1,compound=LEFT,bg='#84a1e6',width=130,command=download_audio)
btn.place(x=850, y=380)



# Function to open PDF
def open_file():
    file_path = filedialog.askopenfilename(
        initialdir=r"C:\Users\kerup\OneDrive\Desktop",
        title="Select PDF or Word file",
        filetypes=(
            ("PDF Files", "*.pdf"),
            ("Word Files", "*.docx"),
            ("All Files", "*.*")
        )
    )

    if not file_path:
        return

    text_area.delete("1.0", END)

    try:
        # PDF FILE
        if file_path.endswith(".pdf"):
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text_area.insert(END, page.extract_text() + "\n")

        # WORD FILE
        elif file_path.endswith(".docx"):
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                text_area.insert(END, para.text + "\n")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to read file\n{e}")



# PDF icon
pdf_icon = r"C:\Users\kerup\OneDrive\Desktop\kiki\python\tkinter dashboard\Images\pdfimage.png"
image_icon2 = tk.PhotoImage(file=pdf_icon)

# KEEP REFERENCE (IMPORTANT)
root.pdf_icon_img = image_icon2

pdf_btn = Button(
    root,
    image=image_icon2,
    bg="#161d3f",
    bd=0,
    command=open_file
)
pdf_btn.place(x=700, y=57)

#music audio

def open_audio():
    audio_path = filedialog.askopenfilename(
        initialdir=r"C:\Users\kerup\OneDrive\Desktop",
        title="Select WAV Audio File",
        filetypes=[("WAV Files", "*.wav")]
    )

    if not audio_path:
        return

    recognizer = sr.Recognizer()
    text_area.delete("1.0", END)
    root.config(cursor="watch")
    root.update_idletasks()

    try:
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)

        # Speech → text
        text = recognizer.recognize_google(audio_data)
        text_area.insert(END, text)


    finally:
        root.config(cursor="")


music_icon = r'C:\Users\kerup\OneDrive\Desktop\kiki\python\tkinter dashboard\Images\music.png'

image_icon3 = tk.PhotoImage(file=music_icon)
root.music_img = image_icon3   # keep reference

btn = Button(
    root,
    image=image_icon3,
    bg='#161d3f',
    bd=0,
    command=open_audio
)
btn.place(x=630, y=57)


otherspeaker_icon = r'C:\Users\kerup\OneDrive\Desktop\kiki\python\tkinter dashboard\Images\otherspeaker.png'
image_icon5 = tk.PhotoImage(file=otherspeaker_icon)
btn=Button(root,compound=LEFT , image=image_icon5 ,bg='#dddaf5',bd=0).place(x=50,y=525)

mic_icon = r'C:\Users\kerup\OneDrive\Desktop\kiki\python\tkinter dashboard\Images\mic.png'
image_icon6 = tk.PhotoImage(file=mic_icon)
btn=Button(root,compound=LEFT , image=image_icon6 ,bg='#cbe7c2',bd=0).place(x=50,y=305)

#pdf and text mode button

button_mode = True
choice = "TEXT"

def changemode():
    global button_mode
    global choice
    if button_mode:
        choice = "PDF"
        mode.config(image=image_icon8,activebackground="white")
        button_mode = False
    else:
        choice = "TEXT"
        mode.config(image=image_icon7)
        button_mode = True

modetext_icon = r'C:\Users\kerup\OneDrive\Desktop\kiki\python\tkinter dashboard\Images\modeText.png'
image_icon7 = tk.PhotoImage(file=modetext_icon)

modepdf_icon = r'C:\Users\kerup\OneDrive\Desktop\kiki\python\tkinter dashboard\Images\modeText.png'
image_icon8 = tk.PhotoImage(file=modepdf_icon)

mode = Button( root,image=image_icon7,bg='#161d3f',bd=0,activebackground="white",command=changemode)
mode.place(x=780, y=40)

root.mainloop()

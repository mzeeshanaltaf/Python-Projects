from tkinter import *
import pandas
from random import choice
from playaudio import playaudio
from gtts import gTTS
import os

# Constant and Globals
BACKGROUND_COLOR = "#B1DDC6"
FLIP_CARD_INTERVAL = 3000  # 3 secs
current_card = {}
to_learn = {}
lang = ""

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer, lang
    window.after_cancel(flip_timer)
    current_card = choice(to_learn)
    canvas.itemconfig(card_background, image=image_front)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    flip_timer = window.after(FLIP_CARD_INTERVAL, func=flip_card)
    lang = 'fr'
    print(lang)


def flip_card():
    global lang
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=image_back)
    lang = 'en'
    print(lang)


def text_to_speech():
    lang_name = ""
    if lang == 'en':
        lang_name = "English"
    elif lang == 'fr':
        lang_name = "French"

    audio_output = gTTS(text=current_card[lang_name], lang=lang)
    audio_output.save("word.mp3")
    playaudio("word.mp3")
    os.remove("word.mp3")


def is_known():
    to_learn.remove(current_card)
    data_f = pandas.DataFrame(to_learn)
    data_f.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(FLIP_CARD_INTERVAL, func=flip_card)

canvas = Canvas(width=800, height=526)
image_front = PhotoImage(file="images/card_front.png")
image_back = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=image_front)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 250, text="", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=3)

cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

speak_image = PhotoImage(file="images/speak.png")
speak_button = Button(image=speak_image, command=text_to_speech)
speak_button.grid(row=1, column=1)

check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=2)

next_card()

window.mainloop()

import streamlit as st
import random
from PIL import Image

st.set_page_config(page_title="Nuotti- ja taukovisa", layout="centered")

# -----------------------------------------
# DATA: Kuva- ja nimilistat
# -----------------------------------------
ITEMS = [
    ("Kokonuotti (1)", "kokonuotti.jpg", 4),
    ("Puolinuotti (1/2)", "puolinuotti.jpg", 2),
    ("Neljäsosanuotti (1/4)", "neljasosanuotti.jpg", 1),
    ("Kahdeksasosanuotti (1/8)", "kahdeksasosanuotti.jpg", 0.5),
    ("Kokotauko (1)", "kokotauko.jpg", 4),
    ("Puolitauko (1/2)", "puolitauko.jpg", 2),
    ("Neljäsosatauko (1/4)", "neljasosatauko.jpg", 1),
    ("Kahdeksasosatauko (1/8)", "kahdeksasosatauko.jpg", 0.5),
]

# -----------------------------------------
# SESSION STATE INIT
# -----------------------------------------
if "playing" not in st.session_state:
    st.session_state.playing = False
if "question_index" not in st.session_state:
    st.session_state.question_index = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "current_question" not in st.session_state:
    st.session_state.current_question = None

# -----------------------------------------
# Start new game
# -----------------------------------------
def start_game():
    st.session_state.playing = True
    st.session_state.question_index = 0
    st.session_state.score = 0
    st.session_state.current_question = None

# -----------------------------------------
# Start screen
# -----------------------------------------
if not st.session_state.playing:
    st.title("🎵 Nuotti- ja taukovisa")
    st.image("images/alku.jpg", width=350)
    st.write("Harjoittele nuottien ja taukojen nimiä sekä aika-arvoja.")
    if st.button("Aloita peli"):
        start_game()
    st.stop()

# -----------------------------------------
# End screen
# -----------------------------------------
if st.session_state.question_index >= 10:
    st.title("Peli päättyi!")
    st.subheader(f"Pisteet: {st.session_state.score} / 10")
    if st.button("Pelaa uudelleen"):
        start_game()
    st.stop()

# -----------------------------------------
# Generate question
# -----------------------------------------
QTYPE = random.choice([1, 2, 3, 4])
correct_item = random.choice(ITEMS)
name, filename, duration = correct_item
wrong_choices = random.sample([i for i in ITEMS if i != correct_item], 3)
choices = [correct_item] + wrong_choices
random.shuffle(choices)
st.session_state.current_question = (correct_item, QTYPE)

st.write(f"**Kysymys {st.session_state.question_index + 1} / 10**")

# -----------------------------------------
# Display question
# -----------------------------------------
if QTYPE == 1:
    st.subheader(f"Valitse kuva: **{name}**")
elif QTYPE == 2:
    st.subheader("Mikä on tämän kuvan nimi?")
    st.image(f"images/{filename}", width=200)
elif QTYPE == 3:
    st.subheader("Mikä on tämän nuotin/tauon aika-arvo?")
    st.image(f"images/{filename}", width=200)
    st.write("(Vastaa numeroa: 4, 2, 1 tai 0.5)")
elif QTYPE == 4:
    st.subheader(f"Valitse kuva aika-arvolle **{duration}**")

# -----------------------------------------
# Answer form
# -----------------------------------------
with st.form("answer_form"):
    user_choice = None
    cols = st.columns(4)

    if QTYPE in [1, 4]:
        # Näytä kuvat + valintapainikkeet
        for i, (n, f, d) in enumerate(choices):
            with cols[i % 4]:
                st.image(f"images/{f}", width=160)
                if st.form_submit_button(n, key=f):
                    user_choice = f

    elif QTYPE == 2:
        choice = st.radio("Valitse oikea nimi:", [c[0] for c in choices])
        submitted = st.form_submit_button("Vastaa")
        if submitted:
            user_choice = choice

    elif QTYPE == 3:
        choice = st.radio("Valitse aika-arvo:", [c[2] for c in choices])
        submitted = st.form_submit_button("Vastaa")
        if submitted:
            user_choice = choice

# -----------------------------------------
# Check answer
# -----------------------------------------
if user_choice:
    correct, qtype = st.session_state.current_question
    correct_name, correct_file, correct_duration = correct

    if qtype in [1, 4]:
        user_item = [i for i in ITEMS if i[1] == user_choice][0]
    elif qtype == 2:
        user_item = [i for i in ITEMS if i[0] == user_choice][0]
    elif qtype == 3:
        user_item = [i for i in ITEMS if i[2] == user_choice][0]

    if user_item == correct:
        st.session_state.score += 1
        st.success("Oikein!")
    else:
        st.error("Väärin.")

    st.session_state.question_index += 1

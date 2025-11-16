import streamlit as st
import random

st.set_page_config(page_title="Nuotti- ja taukovisa", layout="centered")

# -----------------------------------------
# DATA
# -----------------------------------------
NOTES = [
    ("Kokonuotti (1)", "kokonuotti.jpg", 4),
    ("Puolinuotti (1/2)", "puolinuotti.jpg", 2),
    ("Neljäsosanuotti (1/4)", "neljasosanuotti.jpg", 1),
    ("Kahdeksasosanuotti (1/8)", "kahdeksasosanuotti.jpg", 0.5),
]

RESTS = [
    ("Kokotauko (1)", "kokotauko.jpg", 4),
    ("Puolitauko (1/2)", "puolitauko.jpg", 2),
    ("Neljäsosatauko (1/4)", "neljasosatauko.jpg", 1),
    ("Kahdeksasosatauko (1/8)", "kahdeksasosatauko.jpg", 0.5),
]

DURATION_CHOICES = [0.5, 1, 2, 4]
TOTAL_QUESTIONS = 10

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
if "mode" not in st.session_state:
    st.session_state.mode = None  # "notes" or "rests"

# -----------------------------------------
# Start new game
# -----------------------------------------
def start_game(mode):
    st.session_state.playing = True
    st.session_state.question_index = 0
    st.session_state.score = 0
    st.session_state.current_question = None
    st.session_state.mode = mode

# -----------------------------------------
# Sidebar: progress
# -----------------------------------------
if st.session_state.playing:
    st.sidebar.title("📊 Edistyminen")
    progress = st.session_state.question_index / TOTAL_QUESTIONS
    st.sidebar.progress(progress)
    st.sidebar.write(f"Kysymys: {st.session_state.question_index}/{TOTAL_QUESTIONS}")
    st.sidebar.write(f"Pisteet: {st.session_state.score}")

# -----------------------------------------
# Start screen
# -----------------------------------------
if not st.session_state.playing:
    st.title("🎵 Nuotti- ja taukovisa")
    st.image("images/alku.jpg", width=350)
    st.write("Valitse mitä haluat harjoitella:")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Nuotit"):
            start_game("notes")
    with col2:
        if st.button("Tauot"):
            start_game("rests")
    st.stop()

# -----------------------------------------
# End screen
# -----------------------------------------
if st.session_state.question_index >= TOTAL_QUESTIONS:
    st.title("Peli päättyi!")
    st.subheader(f"Pisteet: {st.session_state.score} / {TOTAL_QUESTIONS}")
    if st.button("Pelaa uudelleen"):
        st.session_state.playing = False
    st.stop()

# -----------------------------------------
# Valitaan oikea lista
# -----------------------------------------
ITEMS = NOTES if st.session_state.mode == "notes" else RESTS

# -----------------------------------------
# Generate question
# -----------------------------------------
QTYPE = random.choice([1, 2, 3])  # 1=kuva→nimi, 2=kuva→aika-arvo, 3=nimi→aika-arvo
correct_item = random.choice(ITEMS)
name, filename, duration = correct_item
st.session_state.current_question = (correct_item, QTYPE)

st.write(f"**Kysymys {st.session_state.question_index + 1} / {TOTAL_QUESTIONS}**")

# -----------------------------------------
# Display question
# -----------------------------------------
if QTYPE == 1:
    st.subheader("Mikä on tämän kuvan nimi?")
    st.image(f"images/{filename}", width=200)

elif QTYPE == 2:
    st.subheader("Mikä on tämän kuvan aika-arvo?")
    st.image(f"images/{filename}", width=200)
    st.write("Valitse yksi: 0.5, 1, 2, 4")

elif QTYPE == 3:
    st.subheader(f"Mikä on aika-arvo nimelle **{name}**?")
    st.write("Valitse yksi: 0.5, 1, 2, 4")

# -----------------------------------------
# Answer form
# -----------------------------------------
with st.form("answer_form"):
    user_choice = None

    if QTYPE == 1:
        choice = st.radio("Valitse nimi:", [i[0] for i in ITEMS])
        submitted = st.form_submit_button("Vastaa")
        if submitted:
            user_choice = choice

    elif QTYPE in [2, 3]:
        choice = st.radio("Valitse aika-arvo:", DURATION_CHOICES)
        submitted = st.form_submit_button("Vastaa")
        if submitted:
            user_choice = choice

# -----------------------------------------
# Check answer
# -----------------------------------------
if user_choice is not None:
    correct, qtype = st.session_state.current_question
    correct_name, correct_file, correct_duration = correct

    if qtype == 1:
        is_correct = (user_choice == correct_name)
    else:  # QTYPE 2 or 3
        is_correct = (float(user_choice) == correct_duration)

    if is_correct:
        st.session_state.score += 1
        st.success("Oikein!")
    else:
        st.error(f"Väärin. Oikea vastaus: {correct_duration if qtype != 1 else correct_name}")

    st.session_state.question_index += 1
    st.rerun()
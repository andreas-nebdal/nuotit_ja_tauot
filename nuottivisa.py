import streamlit as st
import random

st.set_page_config(page_title="Nuotti- ja taukovisa", layout="centered")

# -----------------------------------------
# CSS tyylit animaatiolle ja aloitusnäkymälle
# -----------------------------------------
st.markdown(
    """
    <style>
    @keyframes flash {
        0% {opacity: 1;}
        50% {opacity: 0.5;}
        100% {opacity: 1;}
    }
    .flash {
        animation: flash 0.8s ease-in-out 3;
    }
    .title {text-align:center; font-size: 2.5em; font-weight:bold; color:#333;}
    .subtitle {text-align:center; font-size:1.2em; color:#666;}
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------
# DATA
# -----------------------------------------
NOTES = [
    ("Kokonuotti", "kokonuotti.jpg", 4),
    ("Puolinuotti", "puolinuotti.jpg", 2),
    ("Neljäsosanuotti", "neljasosanuotti.jpg", 1),
    ("Kahdeksasosanuotti", "kahdeksasosanuotti.jpg", 0.5),
]

RESTS = [
    ("Kokotauko", "kokotauko.jpg", 4),
    ("Puolitauko", "puolitauko.jpg", 2),
    ("Neljäsosatauko", "neljasosatauko.jpg", 1),
    ("Kahdeksasosatauko", "kahdeksasosatauko.jpg", 0.5),
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
if "questions" not in st.session_state:
    st.session_state.questions = []
if "mode" not in st.session_state:
    st.session_state.mode = None
if "feedback" not in st.session_state:
    st.session_state.feedback = None  # Tallentaa palauteviestin

# -----------------------------------------
# Start new game
# -----------------------------------------
def start_game(mode):
    st.session_state.playing = True
    st.session_state.question_index = 0
    st.session_state.score = 0
    st.session_state.mode = mode
    st.session_state.feedback = None

    ITEMS = NOTES if mode == "notes" else RESTS

    # Luo kaikki mahdolliset parit (item, tyyppi)
    all_pairs = []
    for item in ITEMS:
        for qtype in [1, 2, 3]:  # 1=kuva→nimi, 2=kuva→aika-arvo, 3=nimi→aika-arvo
            all_pairs.append((item, qtype))

    # Arvo 10 uniikkia paria
    st.session_state.questions = random.sample(all_pairs, TOTAL_QUESTIONS)

# -----------------------------------------
# Sidebar progress
# -----------------------------------------
if st.session_state.playing:
    st.sidebar.title("📊 Edistyminen")
    progress = st.session_state.question_index / TOTAL_QUESTIONS
    st.sidebar.progress(progress)
    st.sidebar.write(f"Kysymys: {st.session_state.question_index}/{TOTAL_QUESTIONS}")
    st.sidebar.write(f"Pisteet: {st.session_state.score}")

    # Näytä palaute sivupalkissa
    if st.session_state.feedback:
        color = "#d4edda" if st.session_state.feedback["correct"] else "#f8d7da"
        emoji = "🎉" if st.session_state.feedback["correct"] else "❌"
        st.sidebar.markdown(
            f"""
            <div class="flash" style="background-color:{color}; padding:10px; border-radius:8px; text-align:center; font-size:18px;">
            {emoji} {st.session_state.feedback["message"]}
            </div>
            """,
            unsafe_allow_html=True
        )

# -----------------------------------------
# Start screen
# -----------------------------------------
if not st.session_state.playing:
    st.markdown('<p class="title">🎵 Nuotti- ja taukovisa</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Harjoittele nuottien ja taukojen nimiä sekä aika-arvoja hauskalla tavalla!</p>', unsafe_allow_html=True)

    st.write("Valitse mitä haluat harjoitella:")
    col1, col2 = st.columns(2)

    with col1:
        st.image("images/nuotit.jpg", width=200)
        if st.button("Harjoittele nuotteja"):
            start_game("notes")

    with col2:
        st.image("images/tauot.jpg", width=200)
        if st.button("Harjoittele taukoja"):
            start_game("rests")

    st.stop()

# -----------------------------------------
# End screen
# -----------------------------------------
if st.session_state.question_index >= TOTAL_QUESTIONS:
    st.title("✅ Peli päättyi!")
    st.subheader(f"Pisteet: {st.session_state.score} / {TOTAL_QUESTIONS}")
    if st.button("Pelaa uudelleen"):
        st.session_state.playing = False
    st.stop()

# -----------------------------------------
# Current question
# -----------------------------------------
current_question = st.session_state.questions[st.session_state.question_index]
(correct_item, QTYPE) = current_question
name, filename, duration = correct_item

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
    if QTYPE == 1:
        choice = st.radio("Valitse nimi:", [i[0] for i in (NOTES if st.session_state.mode == "notes" else RESTS)])
    else:
        choice = st.radio("Valitse aika-arvo:", DURATION_CHOICES)

    submitted = st.form_submit_button("Vastaa")

# -----------------------------------------
# Check answer
# -----------------------------------------
if submitted:
    if QTYPE == 1:
        is_correct = (choice == name)
    else:
        is_correct = (float(choice) == duration)

    if is_correct:
        st.session_state.score += 1
        st.success("🎉 Oikein!")
        st.balloons()
        st.session_state.feedback = {"correct": True, "message": "Oikein!"}
    else:
        st.error(f"❌ Väärin! Oikea vastaus: {name if QTYPE == 1 else duration}")
        st.session_state.feedback = {"correct": False, "message": "Väärin!"}

    # Näytä painike seuraavaan kysymykseen
    if st.button("➡ Seuraava kysymys"):
        st.session_state.question_index += 1
        st.session_state.feedback = None
        st.rerun()
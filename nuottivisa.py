import streamlit as st
import random
from PIL import Image
import base64
from io import BytesIO

st.set_page_config(page_title="Nuotti- ja taukovisa", layout="centered")

# -----------------------------------------
# Helper: Make image clickable using HTML
# -----------------------------------------
def clickable_image(image_path, key):
    img = Image.open(image_path)
    buffer = BytesIO()
    img.save(buffer, format="jpg")
    img_b64 = base64.b64encode(buffer.getvalue()).decode()
    html = f"""
        <button style="border:none; background:none;" type="submit" name="choice" value="{key}">
            <img src="data:image/jpg;base64,{img_b64}" width="160">
        </button>
    """
    return html

# -----------------------------------------
# DATA: Kuva- ja nimilistat
# -----------------------------------------

# Nimet ja vastaavat kuvat
ITEMS = [
    # nuotit
    ("Kokonuotti (1)", "kokonuotti.jpg", 4),
    ("Puolinuotti (1/2)", "puolinuotti.jpg", 2),
    ("Neljäsosanuotti (1/4)", "neljasosanuotti.jpg", 1),
    ("Kahdeksasosanuotti (1/8)", "kahdeksasosanuotti.jpg", 0.5),

    # tauot
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
# Show start screen
# -----------------------------------------
if not st.session_state.playing:
    st.title("🎵 Nuotti- ja taukovisa")
    st.image("images/alku.jpg", width=350)
    st.write("Harjoittele nuottien ja taukojen nimiä sekä aika-arvoja.")

    if st.button("Aloita peli"):
        start_game()

    st.stop()


# -----------------------------------------
# END SCREEN
# -----------------------------------------
if st.session_state.question_index >= 10:
    st.title("Peli päättyi!")
    st.subheader(f"Pisteet: {st.session_state.score} / 10")

    if st.button("Pelaa uudelleen"):
        start_game()
    st.stop()


# -----------------------------------------
# Generate a random question
# -----------------------------------------

# random question type:
# 1) show name → choose image
# 2) show image → choose name
# 3) show image → choose duration
# 4) show duration → choose image

QTYPE = random.choice([1, 2, 3, 4])

correct_item = random.choice(ITEMS)
name, filename, duration = correct_item

wrong_choices = random.sample([i for i in ITEMS if i != correct_item], 3)

# shuffle all choices
choices = [correct_item] + wrong_choices
random.shuffle(choices)

# save for checking
st.session_state.current_question = (correct_item, QTYPE)

st.write(f"**Kysymys {st.session_state.question_index + 1} / 10**")

# -----------------------------------------
# DISPLAY QUESTION
# -----------------------------------------

if QTYPE == 1:
    # Name → choose image
    st.subheader(f"Valitse kuva: **{name}**")

elif QTYPE == 2:
    # Image → choose name
    st.subheader("Mikä on tämän kuvan nimi?")
    st.image(f"images/{filename}", width=200)

elif QTYPE == 3:
    # Image → choose duration
    st.subheader("Mikä on tämän nuotin/tauon aika-arvo?")
    st.image(f"images/{filename}", width=200)
    st.write("(Vastaa numeroa: 4, 2, 1 tai 0.5)")

elif QTYPE == 4:
    # Duration → choose image
    st.subheader(f"Valitse kuva aika-arvolle **{duration}**")


# -----------------------------------------
# SHOW CHOICES (clickable images OR buttons)
# -----------------------------------------

with st.form("answer_form"):

    # images as clickable choices
    cols = st.columns(4)

    if QTYPE in [1, 4]:  
        # choose image
        for i, (n, f, d) in enumerate(choices):
            with cols[i % 4]:
                st.markdown(clickable_image(f"images/{f}", key=f), unsafe_allow_html=True)

    elif QTYPE == 2:
        # choose name from buttons
        choice = st.radio("Valitse oikea nimi:", [c[0] for c in choices], index=None)

    elif QTYPE == 3:
        # choose duration
        choice = st.radio("Valitse aika-arvo:", [c[2] for c in choices], index=None)

    submitted = st.form_submit_button("Vastaa")


# -----------------------------------------
# CHECK ANSWER
# -----------------------------------------
if submitted:

    correct, qtype = st.session_state.current_question
    correct_name, correct_file, correct_duration = correct

    user_choice = None

    if qtype in [1, 4]:  
        user_choice = st.session_state.get("choice")
    elif qtype == 2:
        user_choice = choice
    elif qtype == 3:
        user_choice = choice

    # Convert file-based answers
    if qtype in [1, 4]:
        # the user_choice is the filename from the button
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
    st.experimental_rerun()

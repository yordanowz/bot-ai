import streamlit as st
import google.generativeai as genai

# --- 1. CONFIG ---
API_KEY = "AIzaSyDh9IbmNyCxePvhzvXne_G2ndgK2zRMuQw"
genai.configure(api_key=API_KEY)

# --- 2. UI И ПЪЛНО ИЗЧИСТВАНЕ ---
st.set_page_config(page_title="Yordanow AI", page_icon="🤖")

st.markdown("""
<style>
    /* 1. Скрива абсолютно всички стандартни Streamlit компоненти */
    header {visibility: hidden !important;}
    footer {display: none !important;}
    #MainMenu {visibility: hidden !important;}
    .stDeployButton {display:none !important;}
    div.stAppDeployButton {display: none !important;}
    
    /* 2. Скрива логото на Streamlit (червеното кръгче долу вдясно) */
    div[data-testid="stStatusWidget"] {display: none !important;}
    .stApp > header + div {display: none !important;}
    
    /* 3. Дизайн на приложението */
    .main { background-color: #0e1117; color: white; }
    .stChatMessage { border-radius: 15px; border: 1px solid #30363d; background: rgba(255,255,255,0.03); }
    
    /* Скрива и малкия "toolbar" при задържане на мишката върху елементи */
    [data-testid="stElementToolbar"] {display: none !important;}
</style>
""", unsafe_allow_html=True)

# --- 3. MODEL SETUP ---
@st.cache_resource
def get_ai_model():
    try:
        # Използваме 'gemini-1.5-flash' - вече трябва да работи с правилния requirements.txt
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model
    except Exception as e:
        return str(e)

model = get_ai_model()

st.title("🤖 Yordanow AI")

# Проверка за грешки
if isinstance(model, str):
    st.error(f"Грешка при зареждане: {model}")
    st.stop()

# --- 4. CHAT LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Задай ми въпрос..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            answer = response.text
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"Грешка: {str(e)}")

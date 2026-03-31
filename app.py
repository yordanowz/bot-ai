import streamlit as st
import google.generativeai as genai
import os

# --- 1. НАСТРОЙКА НА API ---
API_KEY = "AIzaSyDh9IbmNyCxePvhzvXne_G2ndgK2zRMuQw"
genai.configure(api_key=API_KEY)

# Спираме старите протоколи, които причиняват 404 грешката
os.environ["GOOGLE_API_USE_MTLS"] = "never"

# --- 2. ДИЗАЙН И ПЪЛНО ИЗЧИСТВАНЕ (CSS) ---
st.set_page_config(page_title="Yordanow AI", page_icon="🤖", layout="centered")

st.markdown("""
<style>
    /* Премахва абсолютно всички Streamlit елементи */
    header {visibility: hidden !important;}
    footer {display: none !important;}
    .stAppDeployButton {display:none !important;}
    #MainMenu {visibility: hidden !important;}
    
    /* СКРИВА ЛОГОТО ДОЛУ ДЯСНО (червеното кръгче) */
    div[data-testid="stStatusWidget"] {display: none !important;}
    .stApp > header + div {display: none !important;}
    
    /* Основен черен стил */
    .main { background-color: #0e1117; color: white; }
    .stChatMessage { 
        border-radius: 15px; 
        margin-bottom: 10px; 
        border: 1px solid #30363d; 
        background: rgba(255,255,255,0.03); 
    }
    
    /* Скрива иконите за достъпност и тулбаровете */
    [data-testid="stElementToolbar"] {display: none !important;}
</style>
""", unsafe_allow_html=True)

# --- 3. ЗАРЕЖДАНЕ НА МОДЕЛА ---
@st.cache_resource
def load_ai_model():
    try:
        # Използваме пълното име, за да не се обърква API-то
        return genai.GenerativeModel('models/gemini-1.5-flash')
    except Exception as e:
        return str(e)

model = load_ai_model()

st.title("🤖 Yordanow AI")

# Проверка дали моделът е зареден правилно
if isinstance(model, str):
    st.error(f"Грешка при свързване: {model}")
    st.info("💡 Провери дали си качил requirements.txt в GitHub!")
    st.stop()

# --- 4. ЧАТ ЛОГИКА ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Показване на историята
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Вход за съобщение
if prompt := st.chat_input("Задай ми въпрос..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Генерираме отговора
            response = model.generate_content(prompt)
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.warning("Ботът не върна отговор. Опитай пак.")
        except Exception as e:
            st.error(f"Грешка при генериране: {str(e)}")
            st.info("Ако грешката е 404, добави google-generativeai>=0.5.2 в requirements.txt")

# Странична лента
with st.sidebar:
    st.title("Yordanow AI")
    if st.button("Изчисти историята"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.write("Powered by Yordanow.online")

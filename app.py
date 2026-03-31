import streamlit as st
import google.generativeai as genai
import os

# --- 1. CONFIG ---
API_KEY = "AIzaSyDh9IbmNyCxePvhzvXne_G2ndgK2zRMuQw"
# Насилствено задаваме API версия v1, за да избегнем 404 грешката
os.environ["GOOGLE_API_USE_MTLS"] = "never" 
genai.configure(api_key=API_KEY)

# --- 2. ПЪЛНО ИЗЧИСТВАНЕ НА ИНТЕРФЕЙСА ---
st.set_page_config(page_title="Yordanow AI", page_icon="🤖")

st.markdown("""
<style>
    /* Премахва хедъра, фуутъра и бутона Deploy */
    header {visibility: hidden !important;}
    footer {display: none !important;}
    .stAppDeployButton {display:none !important;}
    #MainMenu {visibility: hidden !important;}
    
    /* Премахва логото на Streamlit долу вдясно (червеното кръгче) */
    div[data-testid="stStatusWidget"] {display: none !important;}
    .stApp > header + div {display: none !important;}
    
    /* Основен стил */
    .main { background-color: #0e1117; color: white; }
    .stChatMessage { border-radius: 15px; border: 1px solid #30363d; background: rgba(255,255,255,0.03); }
</style>
""", unsafe_allow_html=True)

# --- 3. ЗАРЕЖДАНЕ НА МОДЕЛА ---
@st.cache_resource
def load_ai():
    try:
        # Използваме 'gemini-1.5-flash' - вече ще работи с новия requirements.txt
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        return str(e)

model = load_ai()

st.title("🤖 Yordanow AI")

if isinstance(model, str):
    st.error(f"Грешка при свързване: {model}")
    st.stop()

# --- 4. ЧАТ ЛОГИКА ---
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
            # Директно генериране
            response = model.generate_content(prompt)
            answer = response.text
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"Грешка при генериране: {str(e)}")
            st.info("💡 Увери се, че си качил requirements.txt в GitHub!")

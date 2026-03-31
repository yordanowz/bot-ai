import streamlit as st
import google.generativeai as genai

# --- 1. CONFIG ---
# Директно използване на твоя ключ от снимката
API_KEY = "AIzaSyDh9IbmNyCxePvhzvXne_G2ndgK2zRMuQw"
genai.configure(api_key=API_KEY)

# --- 2. MODEL SETUP ---
# Пробваме най-сигурния начин за зареждане
@st.cache_resource
def get_ai_model():
    try:
        # Използваме пълното име на модела
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        return model
    except Exception as e:
        return str(e)

model = get_ai_model()

# --- 3. UI ---
st.set_page_config(page_title="Yordanow AI", page_icon="🤖")

# Скриване на всичко излишно (Deploy, Footer и т.н.)
st.markdown("""
<style>
    header, footer, .stAppDeployButton {visibility: hidden !important;}
    .main { background-color: #0e1117; color: white; }
    .stChatMessage { border-radius: 15px; border: 1px solid #30363d; background: rgba(255,255,255,0.03); }
</style>
""", unsafe_allow_html=True)

st.title("🤖 Yordanow AI")

# Проверка дали моделът е зареден
if isinstance(model, str):
    st.error(f"❌ Грешка при инициализация: {model}")
    st.info("💡 Провери дали в 'requirements.txt' си сложил правилно версията на библиотеката.")
    st.stop()

# --- 4. CHAT LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Показване на съобщенията
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Вход от потребителя
if prompt := st.chat_input("Задай ми въпрос..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Използваме директно генериране
            response = model.generate_content(prompt)
            answer = response.text
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"Грешка при генериране: {str(e)}")

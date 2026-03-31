import streamlit as st
import google.generativeai as genai

# --- 1. НАСТРОЙКА ---
# Твоят API Ключ
GOOGLE_API_KEY = "AIzaSyDh9IbmNyCxePvhzvXne_G2ndgK2zRMuQw"
genai.configure(api_key=GOOGLE_API_KEY)

# --- 2. ДИЗАЙН ---
st.set_page_config(page_title="Yordanow AI", page_icon="🤖")

# Скриваме всичко излишно
st.markdown("""
<style>
    header, footer, .stAppDeployButton {visibility: hidden !important;}
    .main { background-color: #0e1117; color: white; }
    .stChatMessage { border-radius: 15px; border: 1px solid #30363d; background: rgba(255,255,255,0.03); }
</style>
""", unsafe_allow_html=True)

st.title("🤖 Yordanow AI")

# --- 3. ЛОГИКА ЗА МОДЕЛА ---
# Опитваме директно с най-простия метод без сложни инсталации
if "model" not in st.session_state:
    try:
        # Пробваме 'gemini-pro', който е най-съвместим със стари библиотеки
        st.session_state.model = genai.GenerativeModel('gemini-pro')
    except:
        st.session_state.model = None

if "chat" not in st.session_state:
    if st.session_state.model:
        st.session_state.chat = st.session_state.model.start_chat(history=[])
    else:
        st.session_state.chat = None

# --- 4. ЧАТ ИНТЕРФЕЙС ---
if st.session_state.chat is None:
    st.error("❌ Грешка: Проблем с връзката към Google AI. Опитай да обновиш страницата или провери ключа си.")
    st.stop()

# Показване на историята
for message in st.session_state.chat.history:
    with st.chat_message("assistant" if message.role == "model" else "user"):
        st.markdown(message.parts[0].text)

# Вход от потребителя
if prompt := st.chat_input("Пиши тук..."):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Използваме стандартен отговор вместо стрийминг за по-голяма стабилност
            response = st.session_state.chat.send_message(prompt)
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Грешка при генериране: {e}")

# Странична лента
with st.sidebar:
    st.title("Yordanow AI")
    if st.button("Изчисти чата"):
        st.session_state.chat = st.session_state.model.start_chat(history=[])
        st.rerun()

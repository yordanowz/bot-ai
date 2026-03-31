import streamlit as st
import google.generativeai as genai

# --- 1. НАСТРОЙКА НА API ---
GOOGLE_API_KEY = "AIzaSyDh9IbmNyCxePvhzvXne_G2ndgK2zRMuQw"
genai.configure(api_key=GOOGLE_API_KEY)

# --- 2. ИНСТРУКЦИИ ЗА ЛИЧНОСТ ---
SYSTEM_INSTRUCTION = "Ти си Yordanow AI - интелигентен асистент на български език."

# Функция за намиране на работещ модел
@st.cache_resource
def load_model():
    # Списък с възможни имена на модели (от най-новия към по-старите)
    model_names = ['gemini-1.5-flash', 'models/gemini-1.5-flash', 'gemini-pro']
    
    for name in model_names:
        try:
            m = genai.GenerativeModel(model_name=name, system_instruction=SYSTEM_INSTRUCTION)
            # Тестово съобщение, за да видим дали работи
            m.generate_content("test", generation_config={"max_output_tokens": 1})
            return m
        except:
            continue
    return None

model = load_model()

# --- 3. ДИЗАЙН ---
st.set_page_config(page_title="Yordanow AI", page_icon="🤖")

st.markdown("""
<style>
    header, footer, .stAppDeployButton {visibility: hidden !important;}
    .main { background-color: #0e1117; color: white; }
    .stChatMessage { border-radius: 15px; border: 1px solid #30363d; background: rgba(255,255,255,0.03); }
</style>
""", unsafe_allow_html=True)

st.title("🤖 Yordanow AI")

if model is None:
    st.error("❌ Грешка: Не бе намерен активен модел. Провери дали API ключът е активиран в Google AI Studio.")
    st.stop()

# --- 4. ЧАТ СЕСИЯ ---
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

for message in st.session_state.chat_session.history:
    with st.chat_message("assistant" if message.role == "model" else "user"):
        st.markdown(message.parts[0].text)

if prompt := st.chat_input("Пиши тук..."):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        try:
            response = st.session_state.chat_session.send_message(prompt, stream=True)
            for chunk in response:
                full_response += chunk.text
                response_placeholder.markdown(full_response + "▌")
            response_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"Грешка при разговор: {e}")

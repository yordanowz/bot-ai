import streamlit as st
import google.generativeai as genai

# --- 1. CONFIG ---
# Използваме твоя проверен API ключ
API_KEY = "AIzaSyDh9IbmNyCxePvhzvXne_G2ndgK2zRMuQw"
genai.configure(api_key=API_KEY)

# --- 2. ПЪЛНО ИЗЧИСТВАНЕ НА ДИЗАЙНА ---
st.set_page_config(page_title="Yordanow AI", page_icon="🤖")

st.markdown("""
<style>
    /* Премахва абсолютно всичко от Streamlit интерфейса */
    header, footer, .stAppDeployButton, #MainMenu {visibility: hidden !important;}
    div[data-testid="stStatusWidget"] {display: none !important;}
    
    .main { background-color: #0e1117; color: white; }
    .stChatMessage { 
        border-radius: 15px; 
        border: 1px solid #30363d; 
        background: rgba(255,255,255,0.03); 
    }
</style>
""", unsafe_allow_html=True)

# --- 3. УМНО ЗАРЕЖДАНЕ НА МОДЕЛ (План Б) ---
@st.cache_resource
def get_working_model():
    # Опитваме първо с Gemini Pro, защото той е най-стабилен срещу 404 грешки
    models_to_try = ['gemini-pro', 'gemini-1.5-flash', 'models/gemini-1.5-flash']
    for m_name in models_to_try:
        try:
            model = genai.GenerativeModel(m_name)
            # Тест за съвместимост
            model.generate_content("Hi", generation_config={"max_output_tokens": 1})
            return model
        except:
            continue
    return None

model = get_working_model()

st.title("🤖 Yordanow AI")

if model is None:
    st.error("❌ Google все още не активира ключа ти за външни сайтове. Изчакай 1-2 часа или провери ключа в Google AI Studio.")
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
            response = model.generate_content(prompt)
            answer = response.text
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"Грешка: {str(e)}")

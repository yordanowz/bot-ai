import streamlit as st
import google.generativeai as genai

# --- 1. НАСТРОЙКА НА API ---
# Вземи своя ключ от https://aistudio.google.com/
GOOGLE_API_KEY = "AIzaSyDh9IbmNyCxePvhzvXne_G2ndgK2zRMuQw"
genai.configure(api_key=GOOGLE_API_KEY)

# --- 2. ИНСТРУКЦИИ ЗА ЛИЧНОСТ (SYSTEM PROMPT) ---
# Тук програмираме "характера" на бота
SYSTEM_INSTRUCTION = """
Ти си Yordanow AI - високоинтелигентен изкуствен интелект, създаден от Yordanowz.com.
Твоят стил на общуване е:
1. Полезен, директен и професионален.
2. Винаги отговаряш на езика, на който ти говорят (основно български).
3. Можеш да пишеш код, да решаваш задачи и да даваш съвети за бизнес и технологии.
4. Представяш се като Yordanow AI, когато те попитат кой си.
"""

# Инициализиране на модела с инструкциите
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=SYSTEM_INSTRUCTION
)

# --- 3. ДИЗАЙН НА СТРАНИЦАТА ---
st.set_page_config(page_title="Yordanow AI", page_icon="🤖", layout="centered")

st.markdown("""
<style>
    .main { background-color: #0e1117; color: white; }
    /* Скриване на Streamlit логата */
    header {visibility: hidden;}
    footer {display: none;}
    .stAppDeployButton {display:none;}
    
    /* Стил на чат балончетата */
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; border: 1px solid #30363d; }
</style>
""", unsafe_allow_html=True)

st.title("🤖 Yordanow AI")
st.write("Как мога да ти помогна днес?")

# --- 4. ПАМЕТ НА БОТА (CHAT HISTORY) ---
if "chat_session" not in st.session_state:
    # Започваме нова сесия с празна история
    st.session_state.chat_session = model.start_chat(history=[])

# Показваме историята на екрана
for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# --- 5. ЛОГИКА НА РАЗГОВОРА ---
if prompt := st.chat_input("Задай ми въпрос..."):
    # Показваме съобщението на потребителя
    with st.chat_message("user"):
        st.markdown(prompt)

    # Генерираме отговор в реално време (Streaming)
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            # Изпращаме съобщението до Gemini
            response = st.session_state.chat_session.send_message(prompt, stream=True)
            
            for chunk in response:
                full_response += chunk.text
                response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
            
        except Exception as e:
            st.error(f"Грешка при генериране: {e}")

# Странична лента
with st.sidebar:
    st.image("https://yordanowz.com/favicon.ico", width=50) # Сложи линк към твое лого
    st.title("Yordanow AI")
    st.info("Този бот използва Gemini 1.5 Flash - най-новата технология от Google.")
    if st.button("Изчисти разговора"):
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()
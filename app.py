import streamlit as st
import google.generativeai as genai

# --- 1. НАСТРОЙКА НА API ---
# ВНИМАНИЕ: Не споделяй този ключ публично!
GOOGLE_API_KEY = "AIzaSyDh9IbmNyCxePvhzvXne_G2ndgK2zRMuQw"
genai.configure(api_key=GOOGLE_API_KEY)

# --- 2. ИНСТРУКЦИИ ЗА ЛИЧНОСТ ---
SYSTEM_INSTRUCTION = """
Ти си Yordanow AI - високоинтелигентен изкуствен интелект, създаден от Yordanowz.com.
Твоят стил на общуване е:
1. Полезен, директен и професионален.
2. Винаги отговаряш на езика, на който ти говорят (основно български).
3. Пишеш чист код, решаваш задачи и даваш съвети за бизнес.
4. Представяш се като Yordanow AI.
"""

# Използваме 'models/gemini-1.5-flash' - това решава 404 грешката в повечето случаи
try:
    model = genai.GenerativeModel(
        model_name='models/gemini-1.5-flash',
        system_instruction=SYSTEM_INSTRUCTION
    )
except:
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=SYSTEM_INSTRUCTION
    )

# --- 3. ДИЗАЙН НА СТРАНИЦАТА ---
st.set_page_config(page_title="Yordanow AI", page_icon="🤖", layout="centered")

st.markdown("""
<style>
    /* Пълно изчистване на Streamlit интерфейса */
    header {visibility: hidden !important;}
    footer {display: none !important;}
    .stAppDeployButton {display:none !important;}
    #MainMenu {visibility: hidden !important;}
    div[data-testid="stStatusWidget"] {display: none !important;}

    .main { background-color: #0e1117; color: white; }
    
    /* Стил на чат балончетата */
    .stChatMessage { 
        border-radius: 15px; 
        margin-bottom: 10px; 
        border: 1px solid #30363d;
        background-color: rgba(255, 255, 255, 0.03);
    }
</style>
""", unsafe_allow_html=True)

st.title("🤖 Yordanow AI")
st.write("Как мога да ти помогна днес?")

# --- 4. ПАМЕТ НА БОТА ---
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Показваме историята
for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# --- 5. ЛОГИКА НА РАЗГОВОРА ---
if prompt := st.chat_input("Пиши тук..."):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            # Стрийминг на отговора (пише в реално време)
            response = st.session_state.chat_session.send_message(prompt, stream=True)
            
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
            
        except Exception as e:
            # Ако пак има 404, изписваме по-ясно инфо
            st.error(f"Грешка: Моделът не е намерен или API ключът е невалиден. Провери името на модела.")

# Странична лента
with st.sidebar:
    st.title("Yordanow AI")
    st.write("Твоят личен асистент.")
    st.markdown("---")
    if st.button("Изчисти чата"):
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()

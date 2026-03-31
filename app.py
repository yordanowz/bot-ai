import streamlit as st
import google.generativeai as genai
import os

# --- 1. НАСТРОЙКА НА API ---
# Използваме твоя тестван ключ
API_KEY = "AIzaSyDh9IbmNyCxePvhzvXne_G2ndgK2zRMuQw"
genai.configure(api_key=API_KEY)

# Насилствено изключване на стари протоколи за избягване на 404
os.environ["GOOGLE_API_USE_MTLS"] = "never"

# --- 2. ПЪЛНО ИЗЧИСТВАНЕ НА ИНТЕРФЕЙСА (CSS) ---
st.set_page_config(page_title="Yordanow AI", page_icon="🤖", layout="centered")

st.markdown("""
<style>
    /* 1. Скрива горната лента, фуутъра и бутона Deploy */
    header {visibility: hidden !important;}
    footer {display: none !important;}
    .stAppDeployButton {display:none !important;}
    #MainMenu {visibility: hidden !important;}
    
    /* 2. Скрива логото на Streamlit долу вдясно (червеното кръгче) */
    div[data-testid="stStatusWidget"] {display: none !important;}
    .stApp > header + div {display: none !important;}
    
    /* 3. Скрива допълнителни тулбарове и икони */
    [data-testid="stElementToolbar"] {display: none !important;}
    .stDecoration {display:none !important;}

    /* 4. Основен дизайн */
    .main { background-color: #0e1117; color: white; }
    .stChatMessage { 
        border-radius: 15px; 
        margin-bottom: 10px; 
        border: 1px solid #30363d; 
        background: rgba(255,255,255,0.03); 
    }
</style>
""", unsafe_allow_html=True)

# --- 3. ИНИЦИАЛИЗИРАНЕ НА МОДЕЛА ---
@st.cache_resource
def load_ai_model():
    try:
        # Използваме пълното име на модела за максимална съвместимост
        model = genai.GenerativeModel(
            model_name='models/gemini-1.5-flash',
            system_instruction="Ти си Yordanow AI - интелигентен асистент, създаден от Yordanowz.com. Отговаряй винаги на български език по полезен и професионален начин."
        )
        return model
    except Exception as e:
        return str(e)

model = load_ai_model()

# Заглавие на страницата
st.title("🤖 Yordanow AI")

# Проверка дали моделът е зареден правилно
if isinstance(model, str):
    st.error(f"Грешка при свързване: {model}")
    st.info("Увери се, че файлът requirements.txt е качен в GitHub.")
    st.stop()

# --- 4. ЧАТ ИСТОРИЯ И ЛОГИКА ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Показване на предишните съобщения
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Поле за въвеждане на въпрос
if prompt := st.chat_input("Задай ми въпрос..."):
    # Добавяме въпроса на потребителя
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Генериране на отговор
    with st.chat_message("assistant"):
        try:
            # Изпращаме заявката към Gemini
            response = model.generate_content(prompt)
            
            if response.text:
                full_response = response.text
                st.markdown(full_response)
                # Запазваме отговора в историята
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                st.warning("Моделът не върна текст. Опитай отново.")
                
        except Exception as e:
            st.error(f"Грешка при генериране: {str(e)}")
            st.info("Ако виждаш 404, провери дали версията на google-generativeai в requirements.txt е 0.5.2 или по-нова.")

# Странична лента (Sidebar)
with st.sidebar:
    st.title("Управление")
    if st.button("Изчисти чата"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.write("© 2026 Yordanowz.com")

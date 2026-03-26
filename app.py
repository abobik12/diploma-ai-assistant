import streamlit as st
from datetime import datetime
import json
import os

st.set_page_config(page_title="AI Assistant", layout="wide")

DATA_FILE = "data.json"

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({"messages": [], "files": [], "reminders": []}, f, ensure_ascii=False)

def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

data = load_data()

def fake_ai_response(text):
    text_lower = text.lower()

    if "завтра" in text_lower or "напомни" in text_lower or "в " in text_lower:
        return "Похоже, это напоминание. Я могу сохранить его в раздел напоминаний."
    elif "файл" in text_lower or "документ" in text_lower:
        return "Похоже, сообщение связано с файлом или документом."
    else:
        return "Я обработал сообщение как обычную заметку."

st.title("AI Assistant")
st.write("Демо дипломного проекта: личный ассистент с файлами и напоминаниями")

tab1, tab2, tab3 = st.tabs(["Чат", "Файлы", "Напоминания"])

with tab1:
    st.subheader("Чат")

    for msg in data["messages"]:
        with st.chat_message(msg["role"]):
            st.write(msg["text"])
            st.caption(msg["time"])

    user_input = st.chat_input("Напиши сообщение")

    if user_input:
        data["messages"].append({
            "role": "user",
            "text": user_input,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M")
        })

        ai_text = fake_ai_response(user_input)

        data["messages"].append({
            "role": "assistant",
            "text": ai_text,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M")
        })

        save_data(data)
        st.rerun()

with tab2:
    st.subheader("Файлы")

    uploaded_file = st.file_uploader("Загрузи файл")

    if uploaded_file is not None:
        file_info = {
            "filename": uploaded_file.name,
            "uploaded_at": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        data["files"].append(file_info)
        save_data(data)
        st.success(f"Файл {uploaded_file.name} добавлен")
        st.rerun()

    if data["files"]:
        for f in reversed(data["files"]):
            st.write(f"**{f['filename']}**")
            st.caption(f"Загружен: {f['uploaded_at']}")
    else:
        st.write("Файлы пока не загружены")

with tab3:
    st.subheader("Напоминания")

    reminder = st.text_input("Добавить напоминание")

    if st.button("Сохранить напоминание"):
        if reminder.strip():
            data["reminders"].append({
                "text": reminder,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            save_data(data)
            st.success("Напоминание сохранено")
            st.rerun()

    if data["reminders"]:
        for r in reversed(data["reminders"]):
            st.write(f"• {r['text']}")
            st.caption(f"Создано: {r['created_at']}")
    else:
        st.write("Напоминаний пока нет")

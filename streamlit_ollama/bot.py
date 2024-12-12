import streamlit as st
import pandas as pd
import numpy as np
import time
import requests
# Địa chỉ API của Ollama
OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
headers = {"Content-Type": "application/json"}

# Mô hình bạn muốn sử dụng
# model = "llama3.1:8b"
model = "llama3.2:3b"

def query_ollama(prompt , history):
    payload = {
        "model": model,
        "messages": history,
        "stream": False  
    }
    try:
        response = requests.post(OLLAMA_URL, headers=headers, json=payload)
        if response.status_code == 200:
            response_json = response.json()
            return response_json.get("message", {}).get("content", "Không có phản hồi từ bot.")
        else:
            return f"Lỗi API: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Lỗi khi gọi API: {str(e)}"

if "messages" not in st.session_state:
    st.session_state.messages = []  # directory in python


# Hiển thị toàn bộ lịch sử chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


prompt = st.chat_input("Nhập câu hỏi của bạn vào đây !!")


if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
        
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })
      
    
    with st.chat_message("assistant"):
        
        with st.spinner("Đang xử lý ..."):
            response = query_ollama(prompt=prompt , history=st.session_state.messages)
            
        full_response = ""
        holder = st.empty()
                
        for word in response.split():
                    full_response += word + " "
                    time.sleep(0.1)
                    holder.markdown(full_response + "👋")
        holder.markdown(response)
                
        st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })
        
        


#--------------------------------------------------



# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize session state for name if not already set
if "name" not in st.session_state:
    st.session_state.name = ""  # Default value



# Data and UI components
df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
})

df_series = pd.DataFrame({"Contact": ["Email", "Phone", "Social Media"]})

dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20))
)

dataframe2 = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20))
)

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c']
)

map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon']
)

options = st.selectbox("How would you like to be contacted?", df_series["Contact"])
st.write(f'You selected: {options}')

if st.checkbox("Show dataframe"):
    st.write(dataframe2)

# Text input for name
st.text_input("Your name", key="name")  

# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone')
)

# Add a slider to the sidebar:
add_slider = st.sidebar.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0)
)

# Add an input to the sidebar:
add_input = st.sidebar.text_input("Enter value", key="huyr")

if "huyr" not in st.session_state:
    st.session_state.huyr = ""  # Gán giá trị mặc định cho huyr

choose = st.radio("Choose house", ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
st.write(f'Your house choice: {choose}')

#------------------------------------------------------------------------------------------------
x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)

st.title("Interface Chatbox with Streamlit")
st.write(df)
st.dataframe(dataframe.style.highlight_max(axis=0))
st.line_chart(chart_data)
st.map(map_data)

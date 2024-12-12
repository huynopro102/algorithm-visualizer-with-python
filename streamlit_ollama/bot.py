import streamlit as st
import pandas as pd
import numpy as np
import time
import requests
import os
import json
# Địa chỉ API của Ollama
OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
headers = {"Content-Type": "application/json"}


# model = "llama3.1:8b"
model = "llama3.2:3b"

DATA_DIR="chat_data"

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Interface Chatbox with Streamlit")
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



#--------------------- load file from folder to select box -----------------------
chat_files = os.listdir(DATA_DIR)

chat_files = [f for f in chat_files if f.endswith('.json')]

options = ["không dùng dữ liệu"]  + chat_files

add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    options
)

#--------------------- /load file from folder to select box -----------------------



#--------------------- create file.json -----------------------
add_data = st.sidebar.text_input("nhập tên file", key="file_data")

if st.sidebar.button("Tạo tệp mới"):
    if add_data:
        new_file_path = os.path.join(DATA_DIR, f"{add_data}.json")
        if os.path.exists(new_file_path):  # Kiểm tra nếu tệp đã tồn tại
            st.sidebar.error(f"Tệp đã tồn tại: {new_file_path}")
        else:
            with open(new_file_path, 'w') as new_file:
                json.dump(st.session_state.messages, new_file)  # Ghi danh sách dưới dạng JSON
            st.sidebar.success(f"Tệp đã được tạo: {new_file_path}")
    else:
        st.sidebar.error("Vui lòng nhập tên tệp")
#--------------------- /create file.json -----------------------

        

               
#--------------------- load chat history on interface -----------------------

st.sidebar.button("Xóa tệp")
if st.sidebar.button("Tải lịch sử đoạn chat , lên giao diện"):
    if add_selectbox == "không dùng dữ liệu":
        st.sidebar.error("hãy trọn 1 tệp dữ liệu khác")
    else:
        file_path  = os.path.join(DATA_DIR,add_selectbox)
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                st.session_state.messages = json.load(file) 
                st.sidebar.success("load lịch sử đoạn chat thành công")
                
# Hiển thị toàn bộ lịch sử chat ngay lập tức
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
#--------------------- /load chat history on interface -----------------------
      

                
        
        

#---------------------save history chat------------------------------
if st.sidebar.button("Lưu đoạn lịch sử đoạn chat"):
    if add_selectbox == "không dùng dữ liệu":
        st.sidebar.error("hãy trọn 1 tệp dữ liệu khác")
    else:
        file_path  = os.path.join(DATA_DIR,add_selectbox)
        if os.path.exists(file_path):
            with open(file_path, 'w') as file:
                json.dump(st.session_state.messages, file)
                st.sidebar.success(f"lưu đoạn thành công vào {add_selectbox}")
        

#---------------------/save history chat------------------------------





#------------------------------------------------------------------------------------------------

# Add a slider to the sidebar:
add_slider = st.sidebar.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0)
)



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

choose = st.radio("Choose house", ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
st.write(f'Your house choice: {choose}')

x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)

st.write(df)
st.dataframe(dataframe.style.highlight_max(axis=0))
st.line_chart(chart_data)
st.map(map_data)

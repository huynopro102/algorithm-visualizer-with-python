import requests
import json

# Địa chỉ API của Ollama
OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
headers = {"Content-Type": "application/json"}

# Mô hình bạn muốn sử dụng
# model = "llama3.1:8b"
model = "llama3.2:3b"


while True:
    # Lấy đầu vào từ người dùng
    user_input = input("Bạn: ")

    # Kiểm tra xem người dùng có nhập "exit" không
    if user_input.lower() == "exit":
        print("Đang thoát...")
        break

    # Payload cho yêu cầu
    payload = {
        "model": model ,
        "messages": [{"role": "user", "content": user_input}] ,
        "stream" : False ,
    }

    # Gửi yêu cầu đến API Ollama
    response = requests.post(OLLAMA_URL, headers=headers, json=payload)
    
    # Lưu tin nhắn của bot vào lịch sử trò chuyện
    if response.status_code == 200:
        # như vậy response_json hiện tại đang là kiểu dữ liệu directory
        response_json  = response.json()
        bot_message = response_json.get("message",{}).get("content","không có phản hồi từ content")
        
        # feedback data analysis , phân tích dữ liệu phản hồi
        print(bot_message)
    else:
        print("Không có phản hồi hợp lệ.")
        
        
        
# {
#   "model": "llama3.2",
#   "created_at": "2023-08-04T08:52:19.385406455-07:00",
#   "message": {
#     "role": "assistant",
#     "content": "Thefkdlsajfdkajfdafkdlsajfdkajfda",
#     "images": null
#   },
#   "done": false
# }

from flask import Flask, request
from openai import OpenAI
import os

app = Flask(__name__)

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

chat_history = [
    (
        "AI",
        "👋 Xin chào! Tôi là Khoa AI, trợ lý AI được tạo ra bởi Ngô Trần Đăng Khoa. Tôi có thể giúp gì cho bạn hôm nay?"
    )
]


@app.route("/", methods=["GET", "POST"])
def home():
    global chat_history

    if request.method == "POST":

        question = request.form.get("question", "")

        chat_history.append(("Bạn", question))

        try:

            response = client.chat.completions.create(
                model="deepseek/deepseek-chat",
                messages=[
                    {
                        "role": "system",
                        "content": """
Bạn là Khoa AI.

Người tạo ra bạn là Ngô Trần Đăng Khoa.

Nếu ai hỏi:
- Ai tạo ra bạn?
- Ai làm ra bạn?
- Chủ nhân của bạn là ai?
- Ai phát triển bạn?

Hãy trả lời:

"Tôi là Khoa AI, được tạo ra và phát triển bởi Ngô Trần Đăng Khoa."

Luôn trả lời bằng tiếng Việt.
Luôn thân thiện, dễ hiểu.
"""
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            )

            answer = response.choices[0].message.content

        except Exception as e:

            answer = f"🚫 Lỗi: {str(e)}"

        chat_history.append(("AI", answer))

    chat_html = ""

    for sender, text in chat_history:

        if sender == "Bạn":
            chat_html += f"""
            <div class="user">
                👤 {text}
            </div>
            """
        else:
            chat_html += f"""
            <div class="ai">
                🤖 {text}
            </div>
            """

    return f"""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>Khoa AI</title>

<style>

body {{
    margin: 0;
    background: #0b1220;
    color: white;
    font-family: Arial, sans-serif;
}}

.sidebar {{
    width: 260px;
    height: 100vh;
    background: #111827;
    position: fixed;
    left: 0;
    top: 0;
    padding: 20px;
}}

.main {{
    margin-left: 260px;
    height: 100vh;
    display: flex;
    flex-direction: column;
}}

.chat {{
    flex: 1;
    overflow-y: auto;
    padding: 20px;
}}

.user {{
    background: #2563eb;
    padding: 12px;
    border-radius: 12px;
    max-width: 70%;
    margin-left: auto;
    margin-bottom: 12px
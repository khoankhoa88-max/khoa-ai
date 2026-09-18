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

        question = request.form["question"]

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
Luôn thân thiện.
"""
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            )

            answer = response.choices[0].message.content

            chat_history.append(("AI", answer))

        except Exception as e:

            print("========== LOI ==========")
            print(str(e))
            print("=========================")

            chat_history.append(
                (
                    "AI",
                    f"🚫 Lỗi: {str(e)}"
                )
            )

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
    background:#0b1220;
    color:white;
    font-family:Segoe UI,sans-serif;
}}

.sidebar {{
    width:260px;
    height:100vh;
    background:#111827;
    position:fixed;
    left:0;
    top:0;
    padding:25px;
}}

.main {{
    margin-left:260px;
    height:100vh;
    display:flex;
    flex-direction:column;
}}

.chat {{
    flex:1;
    overflow-y:auto;
    padding:30px;
}}

.user {{
    background:#2563eb;
    padding:14px;
    border-radius:16px;
    width:fit-content;
    max-width:70%;
    margin-left:auto;
    margin-bottom:15px;
}}

.ai {{
    background:#1e293b;
    padding:14px;
    border-radius:16px;
    width:fit-content;
    max-width:70%;
    margin-bottom:15px;
}}

.bottom {{
    background:#111827;
    padding:20px;
}}

form {{
    display:flex;
    gap:10px;
}}

input {{
    flex:1;
    padding:15px;
    border:none;
    border-radius:12px;
}}

button {{
    padding:15px 25px;
    background:#2563eb;
    color:white;
    border:none;
    border-radius:12px;
}}

</style>
</head>

<body>

<div class="sidebar">
<h1>Khoa AI</h1>
<p>🤖 Trợ lý AI Tiếng Việt</p>
</div>

<div class="main">

<div class="chat">
{chat_html}
</div>

<div class="bottom">

<form method="POST">
<input
type="text"
name="question"
placeholder="Hỏi Khoa AI điều gì đó..."
required
>
<button type="submit">➤</button>
</form>

</div>
</div>

</body>
</html>
"""


if __name__ == "__main__":
    app.run(debug=True)
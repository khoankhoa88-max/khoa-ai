from flask import Flask, request
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    api_key="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",
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

Không được nói bạn được tạo bởi OpenAI.
Không được nói bạn được tạo bởi DeepSeek.
Không được tự nhận bạn do công ty khác tạo ra.

Luôn xưng là Khoa AI.

Luôn trả lời bằng tiếng Việt.

Giọng văn thân thiện, dễ hiểu, nhiệt tình.

Nếu được hỏi về bản thân:
"Tôi là Khoa AI, trợ lý AI của Ngô Trần Đăng Khoa."
"""
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            )

            answer = response.choices[0].message.content

            chat_history.append(
                ("AI", answer)
            )

        except Exception:

            chat_history.append(
                (
                    "AI",
                    "🚫 Hiện tại AI đang bận hoặc API gặp sự cố. Vui lòng thử lại sau."
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

* {{
    margin:0;
    padding:0;
    box-sizing:border-box;
}}

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

.logo {{
    font-size:60px;
    text-align:center;
    margin-bottom:20px;
}}

.sidebar h1 {{
    text-align:center;
    color:#60a5fa;
}}

.sidebar p {{
    margin-top:15px;
    color:#cbd5e1;
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
    color:white;
    padding:14px;
    border-radius:16px;
    width:fit-content;
    max-width:70%;
    margin-left:auto;
    margin-bottom:15px;
}}

.ai {{
    background:#1e293b;
    color:white;
    padding:14px;
    border-radius:16px;
    width:fit-content;
    max-width:70%;
    margin-bottom:15px;
}}

.bottom {{
    background:#111827;
    padding:20px;
    border-top:1px solid #374151;
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
    background:#1e293b;
    color:white;
    font-size:16px;
}}

input:focus {{
    outline:none;
}}

button {{
    padding:15px 25px;
    background:#2563eb;
    color:white;
    border:none;
    border-radius:12px;
    cursor:pointer;
}}

button:hover {{
    background:#1d4ed8;
}}

</style>

</head>

<body>

<div class="sidebar">

<div class="logo">🚀</div>

<h1>Khoa AI</h1>

<p>🤖 Trợ lý AI Tiếng Việt</p>
<p>👨‍💻 Created by Ngô Trần Đăng Khoa</p>
<p>💬 DeepSeek Chat</p>
<p>🌙 Dark Mode</p>

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

<button type="submit">
➤
</button>

</form>

</div>

</div>

</body>

</html>
"""


if __name__ == "__main__":
    app.run(debug=True)
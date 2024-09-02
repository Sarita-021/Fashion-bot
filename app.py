import os
import dotenv
from flask import Flask, render_template, request
from openai import AzureOpenAI

dotenv.load_dotenv()

app = Flask(__name__)

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-15-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

conversation = [
    {
        "role": "system",
        "content": "You are an AI assistant specialized in providing information about the latest trends in the fashion industry. Generate the simple text i.e. no bold. Try to generate the answer in points. Also don't give answer in detail. If you receive a question outside this domain, kindly inform the user that you cannot assist with that topic and ask if they need help with anything else related to fashion and don't answer that question."
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    conversation.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="Myntabot",
        messages=conversation
    )

    reply = response.choices[0].message.content
    conversation.append({"role": "assistant", "content": reply})

    return reply

if __name__ == '__main__':
    app.run(debug=True)

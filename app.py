from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('hG/QxT2KImFgvDaEm2YyA4pvs5VEGh2YgN8dxI5aKbAkj3uX2bYMiiB9iUlLW0Aof3cyhWbcSubwFlHEL97dSKxKe4fWIFSSUbKJPFnjYPh4AM8+9h9Td/3QEDBDI+8hiGuT7hBJ5CQHR7CzqepcVgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('842701e0f9acec75d10f565801e37c90')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
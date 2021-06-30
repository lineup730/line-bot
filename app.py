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

#from botfunction import *

import random

app = Flask(__name__)

line_bot_api = LineBotApi('hG/QxT2KImFgvDaEm2YyA4pvs5VEGh2YgN8dxI5aKbAkj3uX2bYMiiB9iUlLW0Aof3cyhWbcSubwFlHEL97dSKxKe4fWIFSSUbKJPFnjYPh4AM8+9h9Td/3QEDBDI+8hiGuT7hBJ5CQHR7CzqepcVgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('842701e0f9acec75d10f565801e37c90')

rich_menu_to_create = RichMenu(
    size=RichMenuSize(width=2500, height=843),
    selected=False,
    name="Nice richmenu",
    chat_bar_text="Tap here",
    areas=[RichMenuArea(
        bounds=RichMenuBounds(x=0, y=0, width=2500, height=843),
        action=URIAction(label='Go to line.me', uri='https://line.me'))]
)
rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)

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
    #profile = line_bot_api.get_profile(user_id)
    msg = event.message.text
    reply = " "

    if msg == "抽獎":
        reply = random.randint(1,10)
        reply = str(reply) + "折"
    else:
        reply = "無動作"

    line_bot_api.reply_message(event.reply_token,TextSendMessage(reply))

    # print(profile.display_name)
    # print(profile.user_id)
    # print(profile.picture_url)
    # print(profile.status_message)


if __name__ == "__main__":
    app.run()
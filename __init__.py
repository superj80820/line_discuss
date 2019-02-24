import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)))))
from setting import *
from model.processImage import processImage
from model.db import db
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage
)
processImageModel = processImage()
dbModel = db()
app = Flask(__name__)
line_bot_api = LineBotApi(LINE_TOKEN)
handler = WebhookHandler(LINE_SECRET)

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
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_status = dbModel.selectStatus(event.source.user_id)
    if user_status == "default":
        if event.message.text == "發問":
            dbModel.updateStatus(event.source.user_id, "ask")
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="現在可以開始發問問題了喔~"))
        elif event.message.text == "截圖":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="正在撰寫"))
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="請選擇列表功能喔~"))
    elif user_status == "ask":
        if event.message.text == "結束發問":
            dbModel.updateStatus(event.source.user_id, "default")
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="結束發問囉~"))
        else:
            dbModel.insertDiscuss(event.source.user_id, word_content=event.message.text)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="可以在附加圖片喔 直接上傳即可"))

@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    user_status = dbModel.selectStatus(event.source.user_id)
    if user_status == "ask":
        print("update last discuss : image")
        image_content = processImageModel.lineImageToBase64(
            line_bot_api.get_message_content(event.message.id).iter_content()
        )
        dbModel.updateLastDiscuss(event.source.user_id, "image", image_content)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="已接收到圖片~"))

if __name__ == "__main__":
    app.debug = True
    app.run()
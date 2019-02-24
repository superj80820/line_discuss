import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)))))
from setting import *
from model.processImage import processImage
from model.db import db
from model.imgurApi import imgurApi
import re
import time
from flask import Flask, request, abort, request
from flask_socketio import SocketIO, emit, join_room, rooms
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage,
    ImageSendMessage
)
processImageModel = processImage()
imgurApiModel = imgurApi(CLIENT_ID, CLIENT_SECRET, ACCESS_TOKEN, REFRESH_TOKEN)
dbModel = db()
SID = "ThisISSID"
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
line_bot_api = LineBotApi(LINE_TOKEN)
handler = WebhookHandler(LINE_SECRET)

### line api ###
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
    user_status = dbModel.selectStatusAction(event.source.user_id)
    if user_status == "default":
        if event.message.text == "發問":
            dbModel.updateStatus(event.source.user_id, "action", "ask")
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="現在可以開始發問問題了喔~"))
        elif event.message.text == "截圖":
            room_id = dbModel.selectStatus(event.source.user_id, "room_id")
            socketio.emit('screenshop_requests', {"request" :True, "user_id": event.source.user_id}, room=room_id)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="已經開始截圖 請等待接收~"))
        elif re.search("\d{6}", event.message.text) != None:
            dbModel.updateStatus(event.source.user_id, "room_id", event.message.text)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="已加入會議/課程/簡報~"))
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="請選擇列表功能喔~"))
    elif user_status == "ask":
        if event.message.text == "結束發問":
            dbModel.updateStatus(event.source.user_id, "action", "default")
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
    user_status = dbModel.selectStatusAction(event.source.user_id)
    if user_status == "ask":
        print("update last discuss : image")
        image_content = processImageModel.lineImageToBase64(
            line_bot_api.get_message_content(event.message.id).iter_content()
        )
        dbModel.updateLastDiscuss(event.source.user_id, "image", image_content)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="已接收到圖片~"))

### websocket api ###
@socketio.on('create_room')
def createRoom(room_id):
    print(room_id)
    if dbModel.insertRoom("room_id", room_id):
        join_room(room_id)
        emit('create_room_response', "create room : {}".format(room_id), room=room_id)
    else:
        print("room is exist")

@socketio.on('screenshop_revice')
def screenshopRevice(message):
    print("screenshop revice, user id is : {}".format(message["user_id"]))
    image_name = time.time()
    processImageModel.base64ToImage(image_name, message["image"])
    image_path = "{}.jpg".format(image_name)
    upload_imgur = imgurApiModel.upload(image_path)
    if upload_imgur:
        image_message = ImageSendMessage(
            original_content_url=upload_imgur["link"],
            preview_image_url=upload_imgur["link"]
        )
        line_bot_api.push_message(
            message["user_id"], image_message
        )
    else:
        line_bot_api.push_message(
            message["user_id"], TextSendMessage(text="截圖失敗")
        )
    processImageModel.deleteImage(image_name)

if __name__ == "__main__":
    socketio.run(app, debug = True)
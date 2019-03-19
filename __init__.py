import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)))))
from setting import *
from model.processImage import processImage
from model.db import db
from model.imgurApi import imgurApi
import re
import time
import random
from functional import seq
import json
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
    ImageSendMessage, TemplateSendMessage, ButtonsTemplate, MessageAction,
    PostbackAction, PostbackEvent
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
            dbModel.updateStatus("action", "ask", "user_id", event.source.user_id)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="現在可以開始發問問題了喔~"))
        elif event.message.text == "截圖":
            room_id = dbModel.selectStatus("room_id", "user_id", event.source.user_id)[0][0]
            socketio.emit('screenshop_requests', {"request" :True, "user_id": event.source.user_id}, room=room_id)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="已經開始截圖 請等待接收~"))
        elif re.search("\d{6}", event.message.text) != None:
            dbModel.updateStatus("room_id", event.message.text, "user_id", event.source.user_id)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="已加入會議/課程/簡報~"))
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="請選擇列表功能喔~"))
    elif user_status == "ask":
        if event.message.text == "結束發問":
            dbModel.updateStatus("action", "default", "user_id", event.source.user_id)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="結束發問囉~"))
        else:
            dbModel.insertDiscuss(event.source.user_id, word_content=event.message.text)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="可以在附加圖片喔 直接上傳即可"))

@handler.add(PostbackEvent)
def handle_postback(event):
    user_status = dbModel.selectStatusAction(event.source.user_id)
    req = json.loads(event.postback.data)
    if user_status == "vote":
        vote_data = dbModel.selectVote(req["vote_id"], "vote_data")
        for item in vote_data:
            if item.get(req["item"]) != None:
                item[req["item"]] += 1
        dbModel.updateVote("vote_data", vote_data, "vote_id", req["vote_id"])
        dbModel.updateStatus("action", "default", "user_id", event.source.user_id)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="以投票~"))
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="你已經投票過了喔~"))

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
    join_room(room_id)
    if dbModel.insertRoom("room_id", room_id):
        emit('create_room_response', "create room : {}".format(room_id), room=room_id)
    else:
        emit('create_room_response', "room is exist", room=room_id)

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

@socketio.on('vote')
def voteStart(message):
    if message["action"] == "start":
        print("vote start")
        vote_id = message["vote_id"]
        dbModel.insertVote(message["room_id"], vote_id, [{"item1": 0}, {"item2": 0}])
        dbModel.updateRoom("vote", "start", "room_id", message["room_id"])
        user_id_list = list(seq(dbModel.selectStatus("user_id", "room_id", message["room_id"]))\
            .map(lambda x: x[0]))
        print(message["room_id"])
        vote_template = TemplateSendMessage(
            alt_text='vote template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://image.flaticon.com/icons/png/512/281/281382.png',
                title='來投票囉!',
                text='請選擇',
                actions=[
                    PostbackAction(
                        label='O',
                        data='{"room_id": %s, "vote_id": %s, "item": "item1"}' %(message["room_id"], vote_id)
                    ),
                    PostbackAction(
                        label='X',
                        data='{"room_id": %s, "vote_id": %s, "item": "item2"}' %(message["room_id"], vote_id)
                    )
                ]
            )
        )
        # Need design optimization db function
        for item in user_id_list:
            dbModel.updateStatus("action", "vote", "user_id", item)
        line_bot_api.multicast(
            user_id_list, vote_template
        )
        emit('vote_response', "start vote id : {}".format(message["room_id"]), room=message["room_id"])
    elif message["action"] == "stop":
        print("vote stop")
        dbModel.updateRoom("vote", "stop", "room_id", message["room_id"])
        user_id_list = list(seq(dbModel.selectStatus("user_id", "room_id", message["room_id"]))\
            .map(lambda x: x[0]))
        print(user_id_list)
        vote_data = dbModel.selectVote(message["vote_id"], "vote_data")
        line_bot_api.multicast(
            user_id_list, [
                TextSendMessage(text="投票結束~"),
                TextSendMessage(text="投票結果\nO: {}\nX: {}".format(vote_data[0]["item1"], vote_data[1]["item2"]))]
        )
        emit('vote_response', "stop vote id : {}".format(message["room_id"]), room=message["room_id"])

if __name__ == "__main__":
    socketio.run(app, debug=True)
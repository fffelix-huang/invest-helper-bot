import json

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

line_bot_api = LineBotApi(
    '4MU/F6G3w+2hbFr3aVODdp+rhRlYfN45e/qUuKFtir7jnWnKS11Yu2WvPXOzfLsTbOpbV9qoqGhmtS8DSkl79K1+gKV/xM+mjwQzIOhvOWmLDiAtkrvzqRUrAX8l0gk4DdU4luYGaW3vt4zBJTR5JAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('e49463f8bda3c01f62d9ca4ab65eb33e')


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
    # message: event.message.text
    # user: event.source.userId

    data = json.load(open('data.json', 'r'))

    message = event.message.text
    user = event.source.user_id
    type = message.split(' ')[0]

    if type == "/add":
        if user in data:
            data[user].append({
                "done": False,
                "content": message.split(' ')[1]
            })
        else:
            data[user] = [{
                "done": False,
                "content": message.split(' ')[1]
            }]

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='新增成功')
        )
    elif type == "/del":
        index = int(message.split(' ')[1])
        if user in data:
            del data[user][index]
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='刪除成功')
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='您還沒新增過')
            )
    elif type == "/list":
        if user in data:
            msg = ""
            for i, todo in enumerate(data[user]):
                if todo['done']:
                    msg += f"[{i}] {todo['content']} ✅\n"
                else:
                    msg += f"[{i}] {todo['content']} ❌\n"
            if msg == "":
                msg = "您目前沒有代辦事項"
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=msg)
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='您還沒新增過')
            )
    elif type == "/done":
        index = int(message.split(' ')[1])
        if user in data:
            data[user][index]['done'] = True
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='已紀錄完成')
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='你還沒新增過')
            )

    json.dump(data, open('data.json', 'w'))
    """
    {
        "message": {"id": "16260758267736", "text": "\u4f60\u597d", "type": "text"},
        "mode": "active",
         "replyToken": "63c4a9f92225420dbcc75b5194c74eb8",
         "source": {"type": "user", "userId": "U6761c33c2ec6f168450ccf99fc30d7a4"},
            "timestamp": 1655209804625,
         "type": "message"
    }
    """



if __name__ == "__main__":
    app.run()

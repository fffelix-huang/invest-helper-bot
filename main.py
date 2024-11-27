import json
import os

from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage, TemplateMessage, ButtonsTemplate, MessageAction, URIAction, ImageMessage, PostbackAction, FlexMessage,
    FlexCarousel
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent, PostbackEvent
)
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
# os.getenv("DISCORD_TOKEN")

configuration = Configuration(access_token=os.environ.get('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.environ.get('LINE_CHANNEL_SECRET'))

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
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        if event.message.text == "我不吃牛肉":
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        TextMessage(text='好的，我們將不會提供牛肉給您'),
                        FlexMessage(
                            alt_text='功能表',
                            contents=FlexCarousel.from_json(flex(beef=False))
                        )
                    ]
                )
            )


            return

        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[
                    TemplateMessage(
                        alt_text='功能表',
                        template=ButtonsTemplate(
                            text='請選擇服務項目',
                            actions=[
                                PostbackAction(
                                    label='會員卡',
                                    displayText='顯示會員卡',
                                    data='action=member_card'
                                ),
                            ]
                        )
                    ),
                    TextMessage(text='請選擇你想吃什麼'),
                    FlexMessage(
                        alt_text='功能表',
                        contents=FlexCarousel.from_json(flex())
                    )
                ]
            )
        )


@handler.add(PostbackEvent)
def handle_postback(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        if event.postback.data == 'action=member_card':
            if os.path.exists('static/users.json'):
                users = json.load(open('static/users.json'))
            else:
                users = []

            userId = event.source.user_id
            user_info = list(filter(lambda x: x["id"] == userId, users))

            if len(user_info) == 0:
                user_info = {
                    "id": userId,
                    "name": "未提供",
                }
                users.append(user_info)
                with open("static/users.json", "w") as f:
                    json.dump(users, f)
            else:
                user_info = user_info[0]
            gen_member_card(user_info["name"], userId)
            uid = userId

            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        ImageMessage(
                            original_content_url=f"https://test-linebot.hsuan.app/static/card/{uid}.png",
                            preview_image_url=f"https://test-linebot.hsuan.app/static/card/{uid}.png"
                        ),
                        ImageMessage(
                            original_content_url=f"https://test-linebot.hsuan.app/static/card/{uid}_qr.png",
                            preview_image_url=f"https://test-linebot.hsuan.app/static/card/{uid}_qr.png"
                        )
                    ]
                )
            )







if __name__ == "__main__":
    app.run()

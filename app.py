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

line_bot_api = LineBotApi('GjI1IpKQeZimBizntSLoMqNwbSSltlkZAYdNZeNVOzlQlGpdFdWm+nNJEv4BP0PW4rLW/Lpa5v3K6b1dw7jn8PHU2SvklKO1t00iV0kzM+kOo02jUx2PM1xQ+QACQiB65HF2BsiVg+W3qlJrQXe2rAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('239de2bd219494a2c6bc469a376491ed')


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
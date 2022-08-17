from curses.ascii import isdigit
import os
import re
import json
import random
from unicodedata import digit
from dotenv import load_dotenv
from pyquery import PyQuery
from fastapi import FastAPI, Request, HTTPException
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import ast
import operator

load_dotenv() # Load your local environment variables

CHANNEL_TOKEN = os.environ.get('LINE_TOKEN')
CHANNEL_SECRET = os.getenv('LINE_SECRET')

app = FastAPI()

My_LineBotAPI = LineBotApi(CHANNEL_TOKEN) # Connect Your API to Line Developer API by Token
handler = WebhookHandler(CHANNEL_SECRET) # Event handler connect to Line Bot by Secret key

CHANNEL_ID = os.getenv('LINE_UID') # For any message pushing to or pulling from Line Bot using this ID
# My_LineBotAPI.push_message(CHANNEL_ID, TextSendMessage(text='Welcome !')) # Push a testing message

# Line Developer Webhook Entry Point
@app.post('/')
async def callback(request: Request):
    body = await request.body() # Get request
    signature = request.headers.get('X-Line-Signature', '') # Get message signature from Line Server
    try:
        handler.handle(body.decode('utf-8'), signature) # Handler handle any message from LineBot and 
    except InvalidSignatureError:
        raise HTTPException(404, detail='LineBot Handle Body Error !')
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_textmessage(event):
    global my_calculator

    recieve_equation = str(event.message.text)

    if recieve_equation == '#help':
        command_describtion = '$ Commands:\n\
            <a> + <b>\n\t --> Compute a plus b\n\
            <a> - <b>\n\t --> Compute a minus b\n\
            <a> * <b>\n\t --> Compute a times b\n\
            <a> / <b>\n\t --> Compute a divide by b\n'
        My_LineBotAPI.reply_message(
            event.reply_token,
            TextSendMessage(
                text=command_describtion,
                emojis=[
                    {
                        'index':0,
                        'productId':'5ac21a18040ab15980c9b43e',
                        'emojiId':'110'
                    }
                ]
            )
        )
    else:
        try:
            if recieve_equation.isdigit():
                raise NameError
            ans = eval(recieve_equation)
        except ZeroDivisionError:
            message1 = TextSendMessage(
                       text="$",
                       emojis= [
                                    {
                                        "index": 0,
                                        "productId": "5ac21c46040ab15980c9b442",
                                        "emojiId": "014"
                                    }
                                ]
            )

            message2 = TextSendMessage(text='The division of zero will not succeed, please try another equation!')
            
            My_LineBotAPI.reply_message(
                event.reply_token,
                [message1, message2]
            )
        except (NameError, SyntaxError):
            message1 = TextSendMessage(
                       text="$",
                       emojis= [
                                    {
                                        "index": 0,
                                        "productId": "5ac21c46040ab15980c9b442",
                                        "emojiId": "009"
                                    }
                                ]
            )

            message2 = TextSendMessage(text='It seems like your equation occurs some problem please check out and then try again!\nOr enter "#help" for commands!')
            
            My_LineBotAPI.reply_message(
                event.reply_token,
                [message1, message2]
            )
                    
        else:   
            message1 = TextSendMessage(
                       text="$",
                       emojis= [
                                    {
                                        "index": 0,
                                        "productId": "5ac21d59031a6752fb806d5d",
                                        "emojiId": "005"
                                    }
                                ]
            )

            message2 = TextSendMessage(text=f'Your answer of equation {recieve_equation} is {ans}!')
            
            My_LineBotAPI.reply_message(
                event.reply_token,
                [message1, message2]
            )

class My_Sticker:
    def __init__(self, p_id: str, s_id: str):
        self.type = 'sticker'
        self.packageID = p_id
        self.stickerID = s_id
    
# Add stickers into my_sticker list
stickers_pkg1 = [ My_Sticker(p_id='6362', s_id=str(i)) for i in range(11087920, 11087944)] 
stickers_pkg2 = [ My_Sticker(p_id='6632', s_id=str(i)) for i in range(11825374, 11825398)]
stickers_pkg3 = [ My_Sticker(p_id='8525', s_id=str(i)) for i in range(16581290, 16581314)]
stickers_pkg4 = [ My_Sticker(p_id='11538', s_id=str(i)) for i in range(51626494, 51626534)]
stickers_pkg5 = [ My_Sticker(p_id='789', s_id=str(i)) for i in range(10855, 10895)]

my_sticker = stickers_pkg1 + stickers_pkg2 + stickers_pkg3 + stickers_pkg4 + stickers_pkg5

# Line Sticker Event
@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker(event):
    # Random choice a sticker from my_sticker list
    ran_sticker = random.choice(my_sticker)
    # Reply Sticker Message
    My_LineBotAPI.reply_message(
        event.reply_token,
        StickerSendMessage(
            package_id= ran_sticker.packageID,
            sticker_id= ran_sticker.stickerID
        )
    )


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app='calculator_main:app', reload=True, host='0.0.0.0', port=2022)
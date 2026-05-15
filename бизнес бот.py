from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile, Update
import asyncio
import os
import json
from aiogram.client.session.aiohttp import AiohttpSession
import threading
import  time
import requests

#proxy_url = "socks5://xr7anaad.vpno4ka.xyz:443"

#session = AiohttpSession(proxy=proxy_url)

BOT_TOKEN = "8652604047:AAGp3LkTeHBH0craktt6-8FIR6_954qqEOs"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def ping():
    while True:
        try:
            requests.get('')
        except:
            pass
        time.sleep(600)

threading.Thread(target=ping,daemon=True).start()

def load_conn():
    if os.path.exists('connection.json'):
        with open('connection.json') as f:
            return json.load(f)

    return {}
users_messages = {}
users = load_conn()

@dp.deleted_business_messages()
async def deleted_mess(message):
    print(message)
    mess_id = message.message_ids[0]
    conn_id, text = users_messages[mess_id]
    print(f'удалено сообщние: {text} у пользователя @{users[message.business_connection_id]}')
    await bot.send_message(users[message.business_connection_id],text=f'удалено сообщние: {text}')
    print(mess_id)


@dp.business_connection()
async def conn(connection):
    print('fgqw')
    conn_id = connection.id
    user_id = connection.user.id
    users[conn_id] = user_id
    with open('connection.json','w',encoding='utf-8') as f:
        json.dump(users,f,indent=4)

@dp.business_message()
async def handle(message: types.Message):

    print(f'@{message.from_user.username}  | {message.text}')
    conn_id = message.business_connection_id
    users_messages[message.message_id] = message.business_connection_id,message.text

    if message.business_connection_id and message.reply_to_message and message.reply_to_message.from_user.id != \
            users[conn_id]:
        if message.reply_to_message.video:
            file_id = message.reply_to_message.video.file_id
            file = await bot.get_file(file_id)
            path = "video.mp4"
            await bot.download_file(file.file_path, path,chunk_size=1024*1024)

            await bot.send_video(users[conn_id],video=FSInputFile(path),caption='☝️ скачено с помощью зимних шин')
            os.remove(path)

    if message.business_connection_id and message.reply_to_message and message.reply_to_message.from_user.id != users[conn_id]:
        if message.reply_to_message.photo:

            file_id = message.reply_to_message.photo[-1].file_id
            file = await bot.get_file(file_id)
            path = "photo.jpg"
            await bot.download_file(file.file_path, path,chunk_size=1024*1024)

            await bot.send_photo(users[conn_id], photo=FSInputFile(path),caption='☝️ скачено с помощью зимних шин')
            os.remove(path)






asyncio.run(dp.start_polling(bot))
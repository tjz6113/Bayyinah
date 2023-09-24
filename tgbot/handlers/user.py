import asyncio
import json
from environs import Env
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from ..config import db

user_router = Router()

paths_dict = {
    "01": "NewtoArabic      Done",
    "02": "UnderstandArabic",
    "0101": "TenDaysChallenge    Done",
    "0102": "ReadingFluency     Done",
    "0201": "TheBasics",
    "0202": "TheBasicsandBeyond",
    "020101": "Unit1",
    "020102": "Unit2",
    "020103": "Unit3",
    "020104": "Unit4",
    "020105": "Unit5",
    "020106": "Unit6",
    "020107": "Unit7",
    "020108": "Unit8",
    "020109": "Unit9",
    "020110": "Unit10",
    "020111": "Unit11",
    "020112": "Unit12",
    "020113": "Unit13",
    "020114": "Unit14",
    "020115": "Unit15",
    "020201": "Dream",
    "020202": "ReadingTheClassics       Done",
    "02020101": "BasicNahw",
    "02020102": "BasicSarf",
    "02020103": "AdvancedSarf",
    "02020104": "AdvancedNahw&Structures",
    "02020105": "Balagha",
    "02020106": "BaqarahBeyondTranslation",
    "02020107": "DreamBIG2023"
}





@user_router.message(F.from_user.id == 6625091538, CommandStart())
async def ochopat_start(message: Message):
    await message.reply("Ochopat na gap")
    await asyncio.sleep(5)
    await message.answer("bilaman gulib o'tiribsiz")
    await asyncio.sleep(5)
    await message.answer("yaxshi go'raman sizni ochopat")
    await asyncio.sleep(5)
    await message.answer("siza bir gappim bor")
    await asyncio.sleep(6)
    await message.answer("seryozniy lekin")
    await asyncio.sleep(6)
    await message.answer("dim qatti seryozniy")
    await asyncio.sleep(9)
    await message.answer("sizni dim qatti yaxshi go'raman. xafa bo'lmang lekin")
    await asyncio.sleep(5)
    await message.answer("Xafa bo'lmang yaxshimi?")
    await asyncio.sleep(3)
    await message.answer("Vada baring")
    await asyncio.sleep(15)
    await message.answer("manga turmusha chiqasmi?")
    # await asyncio.sleep(15)



@user_router.message(F.from_user.id == 6625091538)
async def forwardingmessage(message: Message):
    await message.forward(chat_id='6393999936', message_thread_id=message.message_thread_id)

@user_router.message(F.from_user.id == 6393999936)
async def forwardingmessage(message: Message):
    await message.forward(chat_id='6625091538', message_thread_id=message.message_thread_id)


# @user_router.message(CommandStart(), F.chat.id == ochopatID )
# async def user_start(message: Message):
#     await message.reply("Ochopat na gap")
#
#


@user_router.message(F.document.mime_type == "video/mp2t")
async def video_handler(message: Message):
    TFileID = message.document.file_id
    ID = message.document.file_name.split(sep='#')[0]
    items = ID.split(sep='.')
    pathID = items[0]
    VideoID = items[1]
    path = paths_dict[pathID]
    print(path)
    text = f"""
folder - {path}\n
video - {VideoID}\n
"""
    await message.reply(text)

    db.create_table_videos(path)
    db.add_video(path=path, VideoID=VideoID, TFileID=TFileID)


@user_router.message(F.document)
async def file_handler(message: Message):
    data_message = message.dict()
    print(json.dumps(data_message, default=str))

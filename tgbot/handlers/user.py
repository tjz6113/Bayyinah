import json

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from ..config import db

user_router = Router()


@user_router.message(CommandStart())
async def user_start(message: Message):
    await message.reply("Bot started")
paths_dict = {
    "01": "NewtoArabic",
    "02": "UnderstandArabic",
    "0101": "TenDaysChallenge",
    "0102": "ReadingFluency",
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
    "020202": "ReadingTheClassics",
    "02020101": "BasicNahw",
    "02020102": "BasicSarf",
    "02020103": "AdvancedSarf",
    "02020104": "AdvancedNahw&Structures",
    "02020105": "Balagha",
    "02020106": "BaqarahBeyondTranslation",
    "02020107": "DreamBIG2023"
}

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































#
#     filename = message.document.file_name
#     fullID = filename.split(sep='#')[0]
#     parts = fullID.split('_')
#     folder = parts[0]
#     parts = parts[1].split('@')
#     video = parts[0]
#     file = parts[1]
#
#     db.create_table_files(pathID=folder)
#     db.add_file(video, file, message.document.file_id, folder)
#
#
#     text = f"""
# folder - {folder}\n
# video - {video}\n
# file - {file}
# """
#     await message.reply(text)
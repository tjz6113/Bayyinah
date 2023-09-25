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
    "0101": "NewToArabic",
    "0102": "UnderstandArabic",
    "010101": "TenDaysChallenge",
    "010102": "ReadingFluency",
    "010201": "TheBasics",
    "010202": "TheBasicsandBeyond",
    "01020101": "UnitOne",
    "01020102": "UnitTwo",
    "01020103": "UnitThree",
    "01020104": "UnitFour",
    "01020105": "UnitFive",
    "01020106": "UnitSix",
    "01020107": "UnitSeven",
    "01020108": "UnitEight",
    "01020109": "UnitNine",
    "01020110": "UnitTen",
    "01020111": "UnitEleven",
    "01020112": "UnitTwelve",
    "01020113": "UnitThirteen",
    "01020114": "UnitFourteen",
    "01020115": "UnitFifteen",
    "01020201": "Dream",
    "01020202": "ReadingTheClassics",
    "0102020101": "BasicNahw",
    "0102020102": "BasicSarf",
    "0102020103": "AdvancedSarf",
    "0102020104": "AdvancedNahwAndStructures",
    "0102020105": "Balagha",
    "0102020106": "BaqarahBeyondTranslation",
    "0102020107": "DreamBIGTwentyTwentyThree"
}
@user_router.message(F.document.mime_type == "video/mp2ts")
@user_router.message(F.document.mime_type == "video/mp2t")
async def video_handler(message: Message):
    fileID = message.document.file_id
    full_name = message.document.file_name.split(sep='#')
    filename = full_name[1][1:300]
    fullID = full_name[0]
    if fullID.__contains__('_'):
        items = fullID.split(sep='_')
    else:
        items = fullID.split(sep='.')
    folder = items[0]
    video = items[1]
    id = f"{folder}{video}"
    path = paths_dict[folder]
    text = f"""
id - {id}
folder - {path}
video - {video}
filename - {filename}
"""
    await message.reply(text)
    db.add_video(id=id, folder=folder, video=video, filename=filename, fileID=fileID)



@user_router.message(F.document)
async def file_handler(message: Message):
    fileID = message.document.file_id
    full_name = message.document.file_name.split(sep='#')
    filename = full_name[1][1:300]
    fullID = full_name[0]
    if fullID.__contains__('_'):
        items = fullID.split(sep='_')
    else:
        items = fullID.split(sep='.')
    folder = items[0]
    video = items[1].split(sep='@')[0]
    file = items[1].split(sep='@')[1]
    id = f"{folder}{video}{file}"
    path = paths_dict[folder]
    text = f"""
id - {id}
folder - {path}
video - {video}
file - {file}
filename - {filename}
"""
    await message.reply(text)
    db.add_file(id=id, video=video, filename=filename, fileID=fileID)
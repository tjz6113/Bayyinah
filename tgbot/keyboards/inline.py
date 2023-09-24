from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from ..config import paths_dict, kb_dict

def default_kb(folder, start):
    folders = kb_dict[folder]
    kb_list = []
    L = len(folders)
    i = start
    if start + 20 <= L:
        finish = start + 20
    else:
        finish = L
    for i in range(start, finish):
        id = folders[i]
        name = paths_dict[id]
        kb_list.append(InlineKeyboardButton(text=name, callback_data=id))
    if start - 20 > 0:
        kb_list.append(InlineKeyboardButton(text="Previous", callback_data='previous'))
    elif L > start + 20:
        kb_list.append(InlineKeyboardButton(text="Next", callback_data='next'))
    kb = InlineKeyboardMarkup(row_width=2, inline_keyboard=[kb_list])
    return kb

def create_kb(start, count, id_arr, filenames):
    videos_array = []
    for i in range(start, start + 10):
        text = f"{filenames[i]}"
        videos_array.append(InlineKeyboardButton(text=text, callback_data=id_arr[i]))
        
    second_part = []
    if start > 0:
        second_part.append(InlineKeyboardButton(text='Previos', callback_data="previous_videos"))
    second_part.append(InlineKeyboardButton(text='List the names', callback_data="ListNames"))
    if start + 10 < count:
        second_part.append(InlineKeyboardButton(text='Next', callback_data="next_videos"))

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [videos_array[0]],
        [videos_array[1]],
        [videos_array[2]],
        [videos_array[3]],
        [videos_array[4]],
        [videos_array[5]],
        [videos_array[6]],
        [videos_array[7]],
        [videos_array[8]],
        [videos_array[9]],
        second_part
    ])

    return kb

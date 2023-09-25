# importing libraries
from aiogram.utils.keyboard import InlineKeyboardBuilder

# importing main dictionaries
from ..config import paths_dict, kb_dict



async def create_kb(start, folder=None, count=None, id_arr=None, filenames=None, previous_folder=None):
    # deciding to build either keyboard
    if folder is None:
        # assigning values
        if start + 10 > count:
            finish = count
        else:
            finish = start + 10

        # building keyboards
        builder = InlineKeyboardBuilder()
        another_builder = InlineKeyboardBuilder()

        # building keyboard
        for i in range(start, finish):
            text = f"{filenames[i]}"
            builder.button(text=text, callback_data=id_arr[i])
        builder.adjust(1)

        # building another keyboard for management and other functions
        if start > 0:
            another_builder.button(text='Previos', callback_data="previous-videos")
        another_builder.button(text='List the names', callback_data="ListNames")
        if start + 10 < count:
            another_builder.button(text='Next', callback_data="next-videos")
        another_builder.adjust(3)
        if previous_folder is not None:
            another_builder.button(text='Back🔙', callback_data=previous_folder)
        another_builder.button(text='Main Menu🏠', callback_data='00')
        another_builder.adjust(2)

        # attaching the keyboards
        builder.attach(another_builder)

        return builder.as_markup()
    else:
        # assigning the values
        folders = kb_dict[folder]
        L = len(folders)
        i = start
        print(folder)

        # initialising the keyboard builders
        builder = InlineKeyboardBuilder()
        another_builder = InlineKeyboardBuilder()

        # assigning the starting value
        if start + 20 <= L:
            finish = start + 20
        else:
            finish = L

        # building a keyboard
        for i in range(start, finish):
            id = folders[i]
            name = paths_dict[id]
            builder.button(text=name, callback_data=id)
        builder.adjust(1)

        # building another keyboard for better management
        if start - 20 > 0:
            another_builder.button(text="Previous", callback_data='previous')
        if L > start + 20:
            another_builder.button(text="Next", callback_data='next')
        another_builder.adjust(3)




        if folder != '00':
            if folder != '01' or folder != '02':
                if previous_folder is not None:
                    another_builder.button(text='Back🔙', callback_data=previous_folder)
            another_builder.button(text='Main Menu🏠', callback_data='00')
        another_builder.adjust(2)
        # attaching all keyboards
        builder.attach(another_builder)

        return builder.as_markup()


async def after_video_kb():
    # building keyboard
    builder = InlineKeyboardBuilder()

    # creating buttons
    builder.button(text='Previous', callback_data="previous-video")
    builder.button(text='Next', callback_data='next-video')
    builder.button(text='Back🔙', callback_data='back-to-videos-list')
    builder.button(text='Main Menu🏠', callback_data='00')

    return builder.as_markup()

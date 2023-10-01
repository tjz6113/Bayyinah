# importing libraries
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, callback_query
import asyncio

# importing dictionaries
from tgbot.config import paths_dict
# importing filters
from tgbot.filters.admin import AdminFilter

# importing states
from tgbot.misc.states import states

# importing keyboards
from tgbot.keyboards.inline import create_kb, after_video_kb

# importing database
from ..config import db

# assigning the routers
admin_router = Router()
admin_router.message.filter(AdminFilter())




@admin_router.message(Command("send_all"))
async def send_all(message: Message):
    results = db.get_all_videos()

    for result in results:
        await message.answer_video(video=result[0], disable_notification=True)
        asyncio.sleep(0.05)
    
    results = db.get_all_files()

    for result in results:
        await message.answer_document(document=result[0], disable_notification=True)
        asyncio.sleep(0.05)
    


@admin_router.message(F.document.mime_type == "video/mp2ts")
@admin_router.message(F.document.mime_type == "video/mp2t")
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



@admin_router.message(F.document)
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


# start function
@admin_router.message(CommandStart())
async def admin_start(message: Message, state: FSMContext):
    await state.set_state(states.choosing_folder)
    await state.update_data({'indicators': []})
    await message.reply("From which one, would you like to start with?",
                        reply_markup=await create_kb(folder='00', start=0))




@admin_router.callback_query(F.data.in_({'previous-video', 'next-video'}))
async def after_video_handle(call: callback_query.CallbackQuery, state: FSMContext):
    current_video_index = -1000
    # assigning values
    cb = call.data
    data = await state.get_data()
    current_video = data['current-video']
    ids = data['videos-ids']
    first = False
    last = False

    # finding the index of the current video. it helps to locate the id of the other videos
    for index, value in enumerate(ids):
        if value == current_video:
            current_video_index = index


    # taking action based the callback
    if cb == 'back-to-videos-list':
        await backToPreviousFolder(call, state)
    else:
        if cb == 'previous-video':
            current_video = ids[current_video_index - 1]
            if current_video_index == 1:
                first = True  
        elif cb == 'next-video':
            current_video = ids[current_video_index + 1]
            
            if current_video_index +2 == len(ids):
                last = True

        await send_videos(cb=current_video, state=state, call=call, first=first, last=last)
    await state.update_data({'current-video': current_video})


@admin_router.callback_query(F.data == '00')
async def main_menu(call: callback_query.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.set_state(states.choosing_folder)
    await state.update_data({'indicators': []})
    await call.message.answer("From which one, would you like to start with?",
                              reply_markup=await create_kb(folder='00', start=0))


# callback function for going back and forth on the list of folders
@admin_router.callback_query(states.choosing_folder, F.data == 'next')
@admin_router.callback_query(states.choosing_folder, F.data == 'previous')
async def kb_swapping(call: callback_query.CallbackQuery, state: FSMContext):
    # deciding what to do based the callback data
    data = await state.get_data()
    await call.message.delete()

    if call.data == 'back-to-videos-list':
        start = data['start']
    else:
        if call.data == 'next':
            start = data['start'] + 20
        elif call.data == 'previous':
            start = data['start'] - 20

        await state.update_data({'start': start})

    # getting folder id
    folder = data['chosen-folder']
    # sending message to the user with folder as inline keyboard
    await call.message.answer(text="Choose one below", reply_markup=await create_kb(folder=folder, start=start))


@admin_router.callback_query(F.data == 'previous-folder')
async def backToPreviousFolder(call: callback_query.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.set_state(states.choosing_folder)
    # assigning the values
    indicator_line = ''
    data = await state.get_data()
    previous_folder = data['previous-folder']
    indicators = data['indicators']

    # popping out unnecessary data
    cb = previous_folder.pop(-1)
    current_folder = indicators.pop(-1)
    current_folder = indicators[-1] + "\n"  # twice is needed for cutting out unnecessary one and get the needed one
    try:  # building path line
        for value in previous_folder:
            indicator_line = indicator_line + paths_dict[value] + " > "
    except:
        pass
    # sending the message with details
    text = (
        f"<strong><em>{indicator_line}</em></strong>\n\nCurrently showing folders in <strong>{current_folder}</strong>\nChoose one below")
    await call.message.answer(text, reply_markup=await create_kb(folder=cb, start=0))
    await state.update_data({'start': 0, 'chosen-folder': cb, "previous-folder": previous_folder})


# callback function for getting data about requested folder and videos within it
@admin_router.callback_query(states.choosing_folder)
async def get_next_buttons(call: callback_query.CallbackQuery, state: FSMContext):

    # assigning the values
    indicator_line = ''
    cb = call.data
    previous_folder = []
    data = await state.get_data()
    indicators = data['indicators']
    # deleting previous message     
    await call.message.delete()

    # creating path line
    try:
        for value in indicators:
            indicator_line = indicator_line + value + " > "
    except:
        pass

    # getting info about the current folder the user in
    current_folder = paths_dict[str(cb)] + "\n"
    try:
        previous_folder = data['previous-folder']
    except:
        pass
    try:
        previous_folder.append(data['chosen-folder'])
    except:
        pass
    # handling the callback data with try except method. Without error, the try part will send the folders
    # in the requested folder
    try:
        text = f"<strong><em>{indicator_line}</em></strong>\n\nCurrently showing folders in <strong>{current_folder}</strong>\nChoose one below"
        await call.message.answer(text, reply_markup=await create_kb(folder=cb, start=0))
        await state.update_data({'start': 0, 'chosen-folder': cb})
    # except part will send the videos inside the folder
    except KeyError:
        # changing the state 
        await state.set_state(states.showing_videos)
        # assigning the values
        ids = []
        filenames = []
        start = 0

        # getting data from database
        count = db.count_videos(folder=cb)[0]
        result = db.select_videos_for_kb(folder=cb)

        # creating arrays using the data from database
        for value in result:
            ids.append(value[0])
            filenames.append(value[1])

        # storing the values in FSMContext
        await state.update_data({
            'videos-folder': cb,
            'videos-start': start,
            'videos-ids': ids,
            'videos-filenames': filenames,
            'videos-count': count
        })
        # making the text and sending a message with inline keyboard
        text = f"<strong><em>{indicator_line}</em></strong>\n\nCurrently showing videos in <strong>{current_folder}</strong>\nChoose one below"
        await call.message.answer(text=text, reply_markup=await create_kb(start=start, count=count, id_arr=ids,
                                                                          filenames=filenames))

    # storing values in FSMContext
    indicators.append(paths_dict[cb])
    await state.update_data({'indicators': indicators, "previous-folder": previous_folder})


# handling callbacks from videos keyboard
@admin_router.callback_query(states.showing_videos)
@admin_router.callback_query(states.sending_videos, F.data == 'back-to-videos-list')
async def videos_page(call: callback_query.CallbackQuery, state: FSMContext):
    #  assigning values
    cb = call.data
    data = await state.get_data()
    start = data['videos-start']
    count = data['videos-count']
    ids = data['videos-ids']
    filenames = data['videos-filenames']
    current_folder = data['videos-folder']
    await state.update_data({'current-video': cb})
    first = False
    last = False

    await call.message.delete()

    text = f"Videos in {paths_dict[current_folder]} below"
    # checking the callback data and taking action accordingly
    if cb == 'ListNames':
        text = ''
        for name in filenames:
            text = text + name + "\n"
        await call.message.answer(text=text,
                                  reply_markup=await create_kb(start=start, count=count, id_arr=ids,
                                                               filenames=filenames))

    elif cb == "previous-videos":
        start = start - 10
        await call.message.answer(text=text,
                                  reply_markup=await create_kb(start=start, count=count, id_arr=ids,
                                                               filenames=filenames))
    elif cb == "next-videos":
        start = start + 10
        await call.message.answer(text=text,
                                  reply_markup=await create_kb(start=start, count=count, id_arr=ids,
                                                               filenames=filenames))

    elif cb == 'back-to-videos-list':
        await state.set_state(states.showing_videos)
        await call.message.answer(text=text,
                                  reply_markup=await create_kb(start=start, count=count, id_arr=ids,
                                                               filenames=filenames))

    else:
        # now the callback coming is the id for the video.
        # todo. get the file id for both video and file if exits
        # todo. send the video and file to the user with inline buttons asking for next or previous video or back,
        #  or main menu
        # todo. handle the callbacks inside this function
        if ids[0] == cb:
            first = True
        elif ids[-1] == cb:
            last = True
        await send_videos(cb=cb, state=state, call=call, first=first, last=last)


async def send_videos(cb, state, call, first, last):
    # changing the state
    await state.set_state(states.sending_videos)

    # getting the values from database
    video_item = db.select_videos(id=cb)[0]
    videoID = video_item[0]
    video_name = video_item[1]
    result = db.select_files(video=cb)

    # sending video
    await call.message.answer_video(video=videoID, caption=video_name)

    # sending files
    for value in result:
        filename = (value[0])
        fileID = (value[1])
        await call.message.answer_document(caption=filename, document=fileID)

    # sending message with a keyboard
    await call.message.answer(text="Choose the action", reply_markup=await after_video_kb(first, last))
    await state.update_data({"sent-video": cb})

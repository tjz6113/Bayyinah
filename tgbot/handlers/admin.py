# importing libraries
from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, callback_query
from aiogram.methods.send_video import SendVideo
from aiogram.methods.send_document import SendDocument

# importing dictionaries
from tgbot.config import kb_dict, paths_dict
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

state_any = StateFilter('*')


# start function
@admin_router.message(CommandStart())
async def admin_start(message: Message, state: FSMContext):
    await state.set_state(states.choosing_folder)
    await state.update_data({'indicators': []})
    await message.reply("From which one, would you like to start with?",
                        reply_markup=await create_kb(folder='00', start=0))

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
    print("kb_swapping called")
    # deciding what to do based the callback data
    data = await state.get_data()
    await call.message.delete()
    if call.data == 'next':
        start = data['start'] + 20
    else:
        start = data['start'] - 20

    # getting folder id
    folder = data['chosen-folder']
    previous_folder = data['previous-folder']
    # sending message to the user with folder as inline keyboard
    await call.message.answer(text="Choose one below", reply_markup=await create_kb(folder=folder, start=start, previous_folder=previous_folder))


# callback function for getting data about requested folder and videos within it
@admin_router.callback_query(states.choosing_folder)
async def get_next_buttons(call: callback_query.CallbackQuery, state: FSMContext):
    print("get_next_buttons called")
    # assigning the values
    indicator_line = ''
    cb = call.data
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
        previous_folder = data['chosen-folder']
    except KeyError:
        previous_folder = None
        pass
    # handling the callback data with try except method. Without error, the try part will send the folders
    # in the requested folder
    try:
        text = f"<strong><em>{indicator_line}</em></strong>\n\n<strong>{current_folder}</strong>\nChoose one below"
        await call.message.answer(text, reply_markup=await create_kb(folder=cb, start=0, previous_folder=previous_folder))
        await state.update_data({'start': 0, 'chosen-folder': cb, "previous-folder": previous_folder})
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
        print(await state.get_data())
        # making the text and sending a message with inline keyboard
        text = f"<strong><em>{indicator_line}</em></strong>\n\nShowing videos in <strong>{current_folder}</strong> below"
        await call.message.answer(text=text, reply_markup=await create_kb(start=start, count=count, id_arr=ids,
                                                                          filenames=filenames, previous_folder=previous_folder))

    # storing values in FSMContext
    indicators.append(paths_dict[cb])
    await state.update_data({'indicators': indicators})


# handling callbacks from videos keyboard
@admin_router.callback_query(states.showing_videos)
async def send_videos(call: callback_query.CallbackQuery, state: FSMContext):
    print("send_videos called")
    #  assigning values
    cb = call.data
    data = await state.get_data()
    start = data['videos-start']
    count = data['videos-count']
    ids = data['videos-ids']
    filenames = data['videos-filenames']
    current_folder = data['videos-folder']
    previous_folder = data['previous-folder']
    print(previous_folder)

    await call.message.delete()
    # checking the callback data and taking action accordingly
    if cb == "previous-videos":
        start = start - 10
        await call.message.answer(text=f"Videos in {paths_dict[current_folder]} below",
                                  reply_markup=await create_kb(start=start, count=count, id_arr=ids,
                                                               filenames=filenames, previous_folder=previous_folder))
    elif cb == "next-videos":
        start = start + 10
        await call.message.answer(text=f"Videos in {paths_dict[current_folder]} below",
                                  reply_markup=await create_kb(start=start, count=count, id_arr=ids,
                                                               filenames=filenames, previous_folder=previous_folder))
    elif cb == 'ListNames':
        text = ''
        for name in filenames:
            text = text + name + "\n"
        await call.message.answer(text=text, reply_markup=await create_kb(start=start, count=count, id_arr=ids,
                                                                          filenames=filenames, previous_folder=previous_folder))
    else:
        # now the callback coming is the id for the video.
        # todo. get the file id for both video and file if exits
        # todo. send the video and file to the user with inline buttons asking for next or previous video or back,
        #  or main menu
        # todo. handle the callbacks inside this function

        # changing the state
        await state.set_state(states.sending_videos)

        # assigning default values
        filenames, fileID = [], []

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
        await call.message.answer(text="Choose the action", reply_markup=await after_video_kb())

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, callback_query
from ..config import kb_dict, paths_dict

from tgbot.filters.admin import AdminFilter

# importing states
from tgbot.misc.states import states


# importing keyboards
from tgbot.keyboards.inline import default_kb, create_kb


# importing database
from ..config import db


admin_router = Router()
admin_router.message.filter(AdminFilter())



@admin_router.message(CommandStart())
async def admin_start(message: Message, state: FSMContext):
    await state.set_state(states.choosing_folder)
    await message.reply("From which one, would you like to start with?", reply_markup=default_kb(folder='00', start=0))





@admin_router.callback_query(states.choosing_folder, F.data == 'next')
@admin_router.callback_query(states.choosing_folder, F.data == 'previous')
async def kb_swapping(call: callback_query.CallbackQuery, state: FSMContext):
    if call.data == 'next':
        start = await state.get_data('start') + 20
    else:
        start = await state.get_data('start') - 20
    folder = await state.get_data('choosing-folder')
    await call.message.answer(text="Choose one below", reply_markup=default_kb(folder=folder, start=start))


@admin_router.callback_query(states.choosing_folder)
async def get_next_buttons(call: callback_query.CallbackQuery, state: FSMContext):
    global pr_f
    cb = call.data
    print(cb)
    data = await state.get_data()
    try:
        pr_f = data['choosing-folder']
        print(pr_f)
    except KeyError:
        pass
    try:
        try:
            await call.message.delete()
            await call.message.answer(text=f"<strong><em>{paths_dict[data['choosing-folder']]}</em><strong>")
        except Exception:
            print(Exception)
        current_folder = paths_dict[str(cb)] + "\n"
        await call.message.answer(f"<strong>{current_folder}</strong>Choose one below", reply_markup=default_kb(folder=cb, start=0))
        await state.set_data({'start': 0, 'choosing-folder': cb})
    except KeyError:
        await state.set_state(states.showing_videos)
        ids = []
        filenames = []
        count = db.count_videos(folder=cb)[0]
        start = 0
        result = db.select_videos_for_kb(folder=cb)
        for value in result:
            ids.append(value[0])
            filenames.append(value[1])
        await state.update_data(videos_start=start)
        await state.set_data({
            'videos_folder': cb,
            'videos_start': start,
            'videos_ids': ids,
            'videos_filenames': filenames,
            'videos_count': count
        })
        await call.message.answer(text=f"Videos in <strong><em>{paths_dict[cb]}</em></strong> below", reply_markup=create_kb(start, count, ids, filenames))


@admin_router.callback_query(states.showing_videos)
async def send_videos(call: callback_query.CallbackQuery, state: FSMContext):
    cb = call.data
    data = await state.get_data()
    start = data['videos_start']
    count = data['count']
    ids = data['videos_ids']
    filenames = data['videos_filenames']
    if cb == "previous_videos":
        start = start - 10
        await call.message.answer(text=f"Videos in {paths_dict[cb]} below", reply_markup=create_kb(start, count, ids, filenames))
    elif cb == "next_videos":
        start = start + 10
        await call.message.answer(text=f"Videos in {paths_dict[cb]} below", reply_markup=create_kb(start, count, ids, filenames))
    elif cb == 'ListNames':
        text = None
        for name in filenames:
            text = text + name + "\n"
        await call.message.answer(text=text, reply_markup=create_kb(start, count, ids, filenames))





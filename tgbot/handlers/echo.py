from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hcode
import json
from pprint import pprint as print
echo_router = Router()
#
# @echo_router.message(F.text, StateFilter(None))
# async def bot_echo(message: types.Message):
#     text = ["Echo without state.", "Message:", message.text]
#     data_message = message.dict()
#     print(json.dumps(data_message, default=str))
#     await message.answer("\n".join(text))
#
#
# @echo_router.message(F.text)
# async def bot_echo_all(message: types.Message, state: FSMContext):
#     state_name = await state.get_state()
#     text = [
#         f"Echo at the state {hcode(state_name)}",
#         "Place of information:",
#         hcode(message.text),
#     ]
#     await message.answer("\n".join(text))

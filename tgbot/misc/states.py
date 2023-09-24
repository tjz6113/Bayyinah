from aiogram.fsm.state import StatesGroup, State

class states(StatesGroup):
     choosing_folder = State()
     showing_videos = State()
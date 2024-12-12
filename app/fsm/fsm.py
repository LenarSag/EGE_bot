from aiogram.fsm.state import State, StatesGroup


class FSMRegisterForm(StatesGroup):
    fill_first_name = State()
    fill_last_name = State()


class FSMSetScores(StatesGroup):
    set_score = State()
    enter_score = State()
    choose_next = State()

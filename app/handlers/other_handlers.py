from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message


# Инициализируем роутер уровня модуля
router = Router()


# Этот хэндлер будет срабатывать на команду /start вне состояний
# и предлагать перейти к заполнению анкеты, отправив команду /fillform
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(
        text="Этот бот предназначен для регистрации и "
        "сохранения результов ваших экзаменов ЕГЭ\n\n"
        "Чтобы перейти к заполнению анкеты - отправьте команду /register"
        "Чтобы перейти к заполнению баллов - отправьте команду /enter_scores"
    )


# Этот хэндлер будет срабатывать на команду "/cancel" в состоянии
# по умолчанию и сообщать, что эта команда работает внутри машины состояний
@router.message(Command(commands="cancel"), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(
        text=(
            "Чтобы перейти к заполнению анкеты - отправьте команду /register"
            "Чтобы перейти к заполнению баллов - отправьте команду /enter_scores"
        )
    )


# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний
@router.message(Command(commands="cancel"), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text="Вы вышли из заполнения данных\n\n"
        "Чтобы перейти к заполнению анкеты - отправьте команду /register"
        "Чтобы перейти к заполнению баллов - отправьте команду /enter_scores"
    )
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message

from app.crud.user_repository import create_student, get_student_by_id
from app.database.database import async_session
from app.filters.filters import CorrectFirstLastName
from app.fsm.fsm import FSMRegisterForm


# Инициализируем роутер уровня модуля
router = Router()


# Этот хэндлер будет срабатывать на команду /register вне состояний
# и переводить пользователя в меню регистрации
@router.message(Command(commands="register"), StateFilter(default_state))
async def process_fillform_command(message: Message, state: FSMContext):
    async with async_session() as session:
        student = await get_student_by_id(session, message.from_user.id)
        if student:
            return await message.answer(text="Вы уже зарегистрированы")
    await message.answer(text="Пожалуйста, введите ваше имя")
    # Устанавливаем состояние ожидания ввода имени
    await state.set_state(FSMRegisterForm.fill_first_name)


# Этот хэндлер будет срабатывать, если введено корректное имя
@router.message(
    StateFilter(FSMRegisterForm.fill_first_name), CorrectFirstLastName()
)
async def process_first_name_sent(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await message.answer(text="Спасибо!\n\nА теперь введите вашу фамилию")
    # Устанавливаем состояние ожидания ввода фамилии
    await state.set_state(FSMRegisterForm.fill_last_name)


# Этот хэндлер будет срабатывать, если введено некорректное имя
@router.message(StateFilter(FSMRegisterForm.fill_first_name))
async def warning_not_first_name(message: Message):
    await message.answer(
        text=(
            "То, что вы отправили не похоже на имя\n\n"
            "Допускется только кириллица и длина не более 50 \n"
            "Пожалуйста, введите ваше имя\n\n"
            "Если вы хотите прервать заполнение анкеты - "
            "отправьте команду /cancel"
        )
    )


# Этот хэндлер будет срабатывать, если введена корректная фамилия
@router.message(
    StateFilter(FSMRegisterForm.fill_last_name), CorrectFirstLastName()
)
async def process_last_name_sent(message: Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    student_data = await state.get_data()
    student_data["id"] = message.from_user.id

    async with async_session() as session:
        await create_student(session, student_data)
    # Завершаем машину состояний
    await state.clear()
    await message.answer(text="Спасибо! Ваши данные сохранены!\n\n")


# Этот хэндлер будет срабатывать, если введена некорректная фамилия
@router.message(StateFilter(FSMRegisterForm.fill_last_name))
async def warning_last_not_name(message: Message):
    await message.answer(
        text=(
            "То, что вы отправили не похоже на фамилию\n\n"
            "Пожалуйста, введите вашу фамилию\n\n"
            "Допускется только кириллица и длина не более 50"
            "Если вы хотите прервать заполнение анкеты - "
            "отправьте команду /cancel"
        )
    )

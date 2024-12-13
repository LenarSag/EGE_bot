from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message

from app.crud.subject_repository import get_scores
from app.crud.user_repository import get_student_by_id
from app.database.database import async_session


# Инициализируем роутер уровня модуля
router = Router()


# Этот хэндлер будет срабатывать на команду /view_scores вне состояний
# и возвращать оценки пользователя
@router.message(Command(commands="view_scores"), StateFilter(default_state))
async def process_ciew_scores_command(message: Message):
    student_id = message.from_user.id
    async with async_session() as session:
        student = await get_student_by_id(session, student_id)
        if student is None:
            return await message.answer(
                text=(
                    "Вам нужно зарегистрироваться и ввести свои оценки\n"
                    "Чтобы перейти к заполнению анкеты - "
                    "отправьте команду /register"
                    "Чтобы перейти к заполнению баллов - "
                    "отправьте команду /enter_scores"
                )
            )

        results = await get_scores(session, student_id)
        if not results:
            return await message.answer(
                text=(
                    "Вам нужно ввести свои оценки\n"
                    "Чтобы перейти к заполнению баллов - "
                    "отправьте команду /enter_scores"
                )
            )

        scores_message = "Ваши баллы:\n\n"
        scores_message += "\n".join(
            f"{result.subject_name.value}: {result.score}"
            for result in results
        )
        await message.answer(text=scores_message)

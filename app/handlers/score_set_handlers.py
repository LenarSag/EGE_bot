from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message

from app.crud.subject_repository import add_score, get_score, save_all, update_score
from app.crud.user_repository import get_student_by_id
from app.database.database import async_session
from app.keyboard.keyboard import scores_markup, scores_with_option
from app.filters.filters import CorrectSubject
from app.fsm.fsm import FSMSetScores
from config import MAX_SCORE, MIN_SCORE


# Инициализируем роутер уровня модуля
router = Router()


@router.message(Command(commands="enter_scores"), StateFilter(default_state))
async def process_enter_scores_command(message: Message, state: FSMContext):
    async with async_session() as session:
        student = await get_student_by_id(session, message.from_user.id)
        if student is None:
            return await message.answer(
                text=(
                    "Вам нужно зарегистрироваться\n"
                    "Чтобы перейти к заполнению анкеты "
                    "- отправьте команду /register"
                )
            )
    await message.answer(
        text="Пожалуйста, выберите предмет", reply_markup=scores_markup
    )
    # Устанавливаем состояние ожидания выбора предмета
    await state.set_state(FSMSetScores.set_score)


# Этот хэндлер будет срабатывать, если выбран предмет
# и переводит в состояние ввода оценки
@router.callback_query(
    StateFilter(FSMSetScores.set_score),
    CorrectSubject(),
)
async def process_set_score(callback: CallbackQuery, state: FSMContext):
    subject = callback.data
    await state.update_data(subject=subject)

    await callback.message.answer(
        text=f"Спасибо!\n\nА теперь введите ваш балл по {subject}"
    )
    # Устанавливаем состояние ожидания ввода фамилии
    await state.set_state(FSMSetScores.enter_score)


# Этот хэндлер будет срабатывать, если во время выбора предмета
# будет введено/отправлено что-то некорректное
@router.message(StateFilter(FSMSetScores.set_score))
async def warning_set_score(message: Message):
    await message.answer(
        text=(
            "Пожалуйста, пользуйтесь кнопками при выборе предмета\n\n"
            "Если вы хотите прервать заполнение - отправьте "
            "команду /cancel"
        )
    )


# Этот хэндлер будет срабатывать, если введена корректная оценка
# и переводит в состояние выбора опций
@router.message(
    StateFilter(FSMSetScores.enter_score),
    lambda x: x.text.isdigit() and MIN_SCORE <= int(x.text) <= MAX_SCORE,
)
async def process_entered_score(message: Message, state: FSMContext):
    score = int(message.text)

    # получаем название текущего предмета
    data = await state.get_data()
    subject = data.get("subject")

    # Сохраняем баллы за текущий предмет в словарь
    user_scores = data.get("scores", {})
    user_scores[subject] = score
    await state.update_data(scores=user_scores)

    await message.answer(
        text=f"Вы поставили балл {score} по {subject}. "
        "Теперь выберите, что делать дальше.",
        reply_markup=scores_with_option,
    )

    await state.set_state(FSMSetScores.choose_next)


@router.message(StateFilter(FSMSetScores.enter_score))
async def warning_enter_score(message: Message):
    await message.answer(
        text=(
            "Пожалуйста, введите корректную оценку (0 - 100 баллов)\n\n"
            "Если вы хотите прервать заполнение - отправьте "
            "команду /cancel"
        )
    )


@router.callback_query(
    StateFilter(FSMSetScores.choose_next),
    F.data.in_(["next", "stop"]),
)
async def process_choose_next(callback: CallbackQuery, state: FSMContext):
    if callback.data == "next":
        # Продолжаем выбор предметов и выбор оценок
        await callback.message.answer(
            text="Пожалуйста, выберите следующий предмет", reply_markup=scores_markup
        )
        await state.set_state(FSMSetScores.set_score)

    elif callback.data == "stop":
        student_data = await state.get_data()
        student_id = callback.from_user.id

        scores = student_data.get("scores", {})
        # Добавляем оценки в базу данных
        async with async_session() as session:
            for subject, score in scores.items():
                existing_record = await get_score(session, student_id, subject)
                if existing_record:
                    await update_score(session, student_id, subject, score)
                else:
                    await add_score(session, student_id, subject, score)
            await save_all(session)

        # Завершаем машину состояний
        await state.clear()
        await callback.message.answer(text="Спасибо! Ваши данные сохранены!\n\n")


# Этот хэндлер будет срабатывать, если во время выбора дальнейших опций
# будет введено/отправлено что-то некорректное
@router.message(StateFilter(FSMSetScores.choose_next))
async def warning_not_correct_option(message: Message):
    await message.answer(
        text=(
            "Пожалуйста, пользуйтесь кнопками при выборе предмета\n\n"
            "Если вы хотите прервать заполнение - отправьте "
            "команду /cancel"
        )
    )

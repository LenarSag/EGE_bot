from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.models.subject import SubjectName


# Создание кнопок по существующим предметам
buttons_for_subjects = [
    InlineKeyboardButton(text=subject.value, callback_data=subject.value)
    for subject in SubjectName
]
# Создание клавиатуры по кнопкам (по 2 на строку)
keyboard_for_subjects = [
    buttons_for_subjects[i: i + 2] for i in range(
        0, len(buttons_for_subjects), 2
    )
]
scores_markup = InlineKeyboardMarkup(inline_keyboard=keyboard_for_subjects)


# Кнопки "Продолжить" и "Закончить"
stop_enter_scores = [
    InlineKeyboardButton(text="закончить ввод оценок", callback_data="stop")
]
continue_button = [
    InlineKeyboardButton(text="продолжить ввод оценок", callback_data="next")
]

# Создание клавиатуры с опцией выбора дальнейших действий
keyboard_for_next_options = [continue_button, stop_enter_scores]
scores_with_option = InlineKeyboardMarkup(
    inline_keyboard=keyboard_for_next_options
)

import re

from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message

from app.models.subject import SubjectName
from config import FIRST_LAST_NAME_REGEX, MAX_NAME_LENGTH


SUBJECTS = set([subject.value for subject in SubjectName])


class CorrectFirstLastName(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        name = str(message.text)
        return re.match(FIRST_LAST_NAME_REGEX, name) and len(name) <= MAX_NAME_LENGTH


class CorrectSubject(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        subject = str(callback.data)
        return subject in SUBJECTS

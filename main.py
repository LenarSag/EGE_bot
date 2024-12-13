import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from app.handlers import (
    other_handlers,
    score_get_handlers,
    score_set_handlers,
    user_handlers,
)


load_dotenv()


async def main():
    # Инициализируем хранилище
    storage = MemoryStorage()
    # Инициализируем бот и диспетчер
    bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
    dp = Dispatcher(storage=storage)

    # Регистриуем роутеры в диспетчере
    dp.include_router(other_handlers.router)
    dp.include_router(user_handlers.router)
    dp.include_router(score_set_handlers.router)
    dp.include_router(score_get_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

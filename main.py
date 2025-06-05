import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers.admin_handlers import router as admin_router
from handlers.card_handlers import router as card_router

# Настройка логирования
logging.basicConfig(level=logging.INFO)

async def main():
    # Получаем токен бота из переменных окружения
    bot_token = os.getenv("BOT_TOKEN", "your_bot_token_here")
    
    # Создаем экземпляр бота и диспетчера
    bot = Bot(token=bot_token)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    # Регистрируем роутеры
    dp.include_router(admin_router)
    dp.include_router(card_router)
    
    # Запускаем бота
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())

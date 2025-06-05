import os

# Конфигурация бота
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token_here")

# ID первого администратора (создателя бота)
INITIAL_ADMIN_ID = int(os.getenv("INITIAL_ADMIN_ID", "123456789"))

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from storage.data_storage import storage
import asyncio

router = Router()

@router.message(Command("card"))
async def card_command(message: Message):
    """Обработчик команды /card для отправки данных активной карты"""
    
    # Проверяем, есть ли активная карта
    if not storage.has_active_card():
        await message.answer("Активная карта не установлена.")
        return
    
    card_info = storage.get_active_card()
    card_data = card_info["card_data"]
    additional_info = card_info.get("additional_info")
    
    # Формируем сообщение с данными карты
    response = f"Данные карты: `{card_data}`"
    
    # Добавляем дополнительную информацию, если она есть
    if additional_info:
        response += f"\nДополнительная информация: {additional_info}"
    
    # Отправляем сообщение и сохраняем его для последующего удаления
    sent_message = await message.answer(response, parse_mode="Markdown")
    
    # Ждем 10 секунд и удаляем сообщение
    await asyncio.sleep(10)
    await sent_message.delete()

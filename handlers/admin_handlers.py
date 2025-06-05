import re
from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.card_states import CardStates
from storage.data_storage import storage

router = Router()

@router.message(CommandStart(), F.chat.type == "private")
async def start_command(message: Message, state: FSMContext):
    """Обработчик команды /start в личных сообщениях"""
    user_id = message.from_user.id
    
    if not storage.is_admin(user_id):
        await message.answer("У вас нет прав доступа к этому боту.")
        return
    
    # Проверяем, есть ли уже активная карта
    if storage.has_active_card():
        card_info = storage.get_active_card()
        card_data = card_info["card_data"]
        additional_info = card_info.get("additional_info")
        
        # Формируем сообщение с текущей картой
        response = f"Актуальная карта: `{card_data}`"
        if additional_info:
            response += f"\nДополнительная информация: {additional_info}"
        response += "\n\nЖелаете добавить новую? (- если нет)"
        
        await message.answer(response, parse_mode="Markdown")
        await state.set_state(CardStates.waiting_for_card_data)
    else:
        await message.answer("Здравствуйте! Введите данные карты:")
        await state.set_state(CardStates.waiting_for_card_data)

@router.message(CardStates.waiting_for_card_data, F.chat.type == "private")
async def process_card_data(message: Message, state: FSMContext):
    """Обработчик ввода данных карты"""
    user_id = message.from_user.id
    
    if not storage.is_admin(user_id):
        await message.answer("У вас нет прав доступа к этому боту.")
        await state.clear()
        return
    
    card_data = message.text.strip() if message.text else ""
    
    # Если пользователь ввел "-", отменяем добавление новой карты
    if card_data == "-":
        await message.answer("Добавление новой карты отменено.")
        await state.clear()
        return
    
    await state.update_data(card_data=card_data)
    
    await message.answer("Желаете добавить дополнительную информацию? (Если нет введите -)")
    await state.set_state(CardStates.waiting_for_additional_info)

@router.message(CardStates.waiting_for_additional_info, F.chat.type == "private")
async def process_additional_info(message: Message, state: FSMContext):
    """Обработчик ввода дополнительной информации"""
    user_id = message.from_user.id
    
    if not storage.is_admin(user_id):
        await message.answer("У вас нет прав доступа к этому боту.")
        await state.clear()
        return
    
    additional_info = message.text.strip() if message.text else ""
    data = await state.get_data()
    card_data = data.get("card_data")
    
    # Если пользователь ввел "-" или пустую строку, дополнительную информацию не сохраняем
    if additional_info == "-" or not additional_info:
        additional_info = None
    
    # Сохраняем карту как активную
    storage.set_active_card(card_data, additional_info)
    
    await message.answer("Карта успешно добавлена как активная!")
    await state.clear()

@router.message(Command("addadmin"), F.chat.type == "private")
async def add_admin_command(message: Message):
    """Обработчик команды /addadmin для добавления нового администратора"""
    user_id = message.from_user.id
    
    if not storage.is_admin(user_id):
        await message.answer("У вас нет прав для выполнения этой команды.")
        return
    
    # Извлекаем ID нового администратора из команды
    command_parts = message.text.split()
    if len(command_parts) != 2:
        await message.answer("Использование: /addadmin {user_id}")
        return
    
    try:
        new_admin_id = int(command_parts[1])
    except ValueError:
        await message.answer("ID пользователя должен быть числом.")
        return
    
    # Добавляем нового администратора
    if storage.add_admin(new_admin_id):
        await message.answer(f"Пользователь {new_admin_id} успешно добавлен как администратор.")
    else:
        await message.answer(f"Пользователь {new_admin_id} уже является администратором.")

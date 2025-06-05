from typing import Dict, Set, Optional
from config import INITIAL_ADMIN_ID

class DataStorage:
    def __init__(self):
        # Множество ID администраторов
        self.admins: Set[int] = {INITIAL_ADMIN_ID}
        
        # Данные активной карты
        self.active_card: Optional[Dict[str, str]] = None
    
    def is_admin(self, user_id: int) -> bool:
        """Проверяет, является ли пользователь администратором"""
        return user_id in self.admins
    
    def add_admin(self, user_id: int) -> bool:
        """Добавляет нового администратора"""
        if user_id not in self.admins:
            self.admins.add(user_id)
            return True
        return False
    
    def set_active_card(self, card_data: str, additional_info: Optional[str] = None):
        """Устанавливает активную карту"""
        self.active_card = {
            "card_data": card_data,
            "additional_info": additional_info
        }
    
    def get_active_card(self) -> Optional[Dict[str, str]]:
        """Возвращает данные активной карты"""
        return self.active_card
    
    def has_active_card(self) -> bool:
        """Проверяет, есть ли активная карта"""
        return self.active_card is not None

# Глобальный экземпляр хранилища
storage = DataStorage()

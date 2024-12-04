from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.logs_repository import LogsRepository

class LogService:
    '''
    Класс сервиса для работы с логами
    
    Атрибуты:
    session [:AsyncSession] - сессия базы данных
    logs_repository [:LogsRepository] - репозиторий логов
    
    Методы:
    get_logs_by_adress - функция получения логов по адресу
    '''
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.logs_repository = LogsRepository(session)
    
    async def get_logs_by_adress(self, adress: str, limit: int = 100) -> list:
        '''
        Функция получения логов по адресу
        
        Параметры:
        adress [:str] - адрес
        limit [:int] - лимит логов

        Возвращает:
        logs [:list] - список логов
        '''
        logs = await self.logs_repository.get_logs_by_adress(adress)
        messages = await self.logs_repository.get_messages_by_adress(adress)
        
        combined_logs = logs + messages
        combined_logs.sort(key=lambda x: (x['timestamp'], x['int_id']), reverse=True)
        return combined_logs[:limit]
    
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy import func
import logging

from app.models.log import Message, Log


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LogsRepository:
    '''
    Класс репозитория для работы с таблицами message и log
    
    Атрибуты:
    session [:AsyncSession] - сессия базы данных
    
    Методы:
    insert_message - процедура вставки сообщения в таблицу message
    insert_log - процедура вставки лога в таблицу log
    
    '''
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def insert_message(self, message: dict):
        '''
        Процедура вставки сообщения в таблицу message
        
        Параметры:
        message [:dict] - словарь данных
        '''
        try:
            new_message = Message(**message)
            self.session.add(new_message)
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error inserting message: {e}, data: {new_message}")
            raise
        
    async def insert_log(self, log: dict) -> None:
        '''
        Процедура вставки лога в таблицу log
        
        Параметры:
        log [:dict] - словарь данных
        '''
        try:
            new_log = Log(**log)
            self.session.add(new_log)
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error inserting message: {e}, data: {new_log}")
            raise

    async def get_logs_by_adress(self, adress: str, limit: int = 100) -> list:
        '''
        Функция получения логов по адресу
        
        Параметры:
        adress [:str] - адрес
        
        Возвращает:
        logs [:list] - список логов
        '''
        try:
            query = (
                select(
                Log.created.label('timestamp'),
                Log.str.label('log_entry'),
                Message.int_id,
                )
                .join(Message, Log.int_id == Message.int_id, isouter=True)
                .where(Message.str == adress)
                .order_by(Log.created.desc())
                .limit(10)
                )

            result = await self.session.execute(query)
            logs = result.scalars().all()
            return logs


        except NoResultFound:
            logger.error(f"Logs not found by adress: {adress}")
            return None
        except Exception as e:
            logger.error(f"Error getting logs by adress: {e}")
            raise
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
    def __init__(self, session: AsyncSession):
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
        
    async def insert_log(self, log: dict):
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
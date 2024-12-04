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
    check_logs - функция проверки наличия логов
    cheсk_messages - функция проверки наличия сообщений
    get_logs_by_adress - функция получения логов по адресу получателя
    get_messages_by_adress - функция получения сообщений по адресу получателя
    '''
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def insert_message(self, message: dict):
        '''
        Процедура вставки сообщения в таблицу message
        
        Параметры:
        message [:dict] - словарь данных сообщения
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
        log [:dict] - словарь данных лога
        '''
        try:
            new_log = Log(**log)
            self.session.add(new_log)
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error inserting message: {e}, data: {new_log}")
            raise

    async def check_logs(self) -> bool:
        '''
        Функция проверки наличия логов
        
        Возвращает:
        result [:bool] - результат проверки
        '''
        try:
            query = select(func.count(Log.int_id))
            result = await self.session.execute(query)
            count = result.scalar()
            return count > 0
        except Exception as e:
            logger.error(f"Error checking logs: {e}")
            raise
    
    async def cheсk_messages(self) -> bool:
        '''
        Функция проверки наличия сообщений 
        
        Возвращает:
        result [:bool] - результат проверки 
        '''
        try:
            query = select(func.count(Message.int_id))
            result = await self.session.execute(query)
            count = result.scalar()
            return count > 0
        except Exception as e:
            logger.error(f"Error checking messages: {e}")
            raise

    async def get_logs_by_adress(self, adress: str) -> list:
        '''
        Функция получения логов по адресу получателя
        
        Параметры:
        adress [:str] - адрес получателя
        
        Возвращает:
        logs [:list] - список логов
        '''
        try:
            query = (
                select(
                Log.created.label('timestamp'),
                Log.str.label('log_entry'),
                Log.int_id,
                )
                .where(Log.address == adress)
            )

            result = await self.session.execute(query)
            logs = result.fetchall()
            return [{'timestamp': log.timestamp, 'log_entry': log.log_entry, 'int_id': log.int_id} for log in logs]
        
        except NoResultFound:
            logger.error(f"Logs not found by adress: {adress}")
            return None
        except Exception as e:
            logger.error(f"Error getting logs by adress: {e}")
            raise

    async def get_messages_by_adress(self, adress: str) -> list:
        '''
        Функция получения сообщений по адресу получателя
        
        Параметры:
        adress [:str] - адрес получателя
        
        Возвращает:
        messages [:list] - список сообщений
        '''
        
        try:
            query = (
                select(
                Message.created.label('timestamp'),
                Message.str.label('log_entry'),
                Message.int_id,
                )
                .join(Log, Message.int_id == Log.int_id)
                .where(Log.address == adress)
            )

            result = await self.session.execute(query)
            messages = result.fetchall()
            return [{'timestamp': message.timestamp, 'log_entry': message.log_entry, 'int_id': message.int_id} for message in messages]

        except NoResultFound:
            logger.error(f"Logs not found by adress: {adress}")
            return None
        except Exception as e:
            logger.error(f"Error getting logs by adress: {e}")
            raise
from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, Index, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base


class Message(Base):
    """
    Модель сообщения в системе.

    Атрибуты:
        created (datetime): Время создания сообщения (timestamp строки лога).
        id (str): Внешний идентификатор сообщения (например, id=xxxx).
        int_id (str): Внутренний ID сообщения.
        str (str): Текст сообщения.
        status (bool): Статус сообщения (? не понятен смысл, но добавил согласно тз)
    """
    __tablename__ = "message"

    created = Column(DateTime, default=datetime.now, index=True)
    id = Column(String, primary_key=True, index=True)
    int_id = Column(String(16), index=True)
    str = Column(String)
    status = Column(Boolean)
    
    def __repr__(self):
        return f"<Message {self.id}>"


class Log(Base):
    """
    Модель лога.

    Атрибуты:
        id (str): ID строки лога.
        created (datetime): Время создания строки лога.
        int_id (str): Внутренний ID сообщения, связанный с логом.
        str (str): Текст строки лога (без временной метки).
        address (str): Адрес получателя.
    """
    __tablename__ = "log"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    created = Column(DateTime, default=datetime.now, index=True)
    int_id = Column(String(16), index=True)
    str = Column(String)
    address = Column(String)
    
    # Хэш-индекс для ускорения поиска по адресу
    __table_args__ = (
        Index('log_address_idx', 'address', postgresql_using='hash'),
    )

    def __repr__(self):
        return f"<Log {self.int_id}>"

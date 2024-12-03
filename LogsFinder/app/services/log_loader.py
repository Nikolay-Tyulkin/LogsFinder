import logging
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.logs_repository import LogsRepository
from app.repositories.log_parser import LogParser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LogLoader:
    """
    Класс загрузки логов в базу данных.

    Атрибуты:
        logs_path (str): Путь к файлу логов.
        logs_repository (LogsRepository): Репозиторий для работы с логами.
        log_parser (LogParser): Парсер логов.
    """

    def __init__(self, logs_path: str, session: AsyncSession):
        self.logs_path = logs_path
        self.logs_repository = LogsRepository(session=session)
        self.log_parser = LogParser(log_path=logs_path)

    async def load_logs(self):
        """
        Асинхронная процедура загрузки логов в базу данных.
        """
        logs_counter = {
            'message': 0,
            'log': 0,
            'non_format': 0
        }

        for line in self.log_parser.parse_log_file():  # Если парсер асинхронный
            line_list = line.split(' ')
            if self.log_parser.id_int_check(line_list):
                if self.log_parser.format_check(line_list):
                    if line_list[3] == '<=':
                        message = self.log_parser.prepare_message(line_list)
                        await self.logs_repository.insert_message(message)  # Добавлено await
                        logs_counter['message'] += 1
                    else:
                        log = self.log_parser.prepare_log(line_list)
                        await self.logs_repository.insert_log(log)  # Добавлено await
                        logs_counter['log'] += 1
                else:
                    log = self.log_parser.prepare_non_format(line_list)
                    await self.logs_repository.insert_log(log)  # Добавлено await
                    logs_counter['log'] += 1
            else:
                logs_counter['non_format'] += 1

        logger.info(f"Logs loaded: {logs_counter}")

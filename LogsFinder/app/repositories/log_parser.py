import datetime

class LogParser:
    '''
    Класс парсинга логов
    
    Атрибуты:
        log_path [:str] - Путь к файлу логов
        
    Методы:
        parse_log_file: генератор для чтения файла логов
        id_int_check: проверка на длину ID и его корректность
        format_check: проверка на правильность формата строки
        prepare_message: подготовка сообщения
        prepare_log: подготовка лога
        prepare_non_format: подготовка не правильной по формату строки
    '''
    def __init__(self, log_path: str):
        self.log_path = log_path
        
    def parse_log_file(self):
        '''
        Генератор для чтения файла логов
        '''
        with open(self.log_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    yield line
                    
    def id_int_check(self, line_list: list) -> bool:
        '''
        Проверка на длину ID и его корректность
        
        Параметры:
        line_list [:list] - список строк
        
        Возвращает:
        bool - результат проверки
        '''
        if len(line_list[2]) != 16:
            return False
        else:
            return True
        
    def format_check(self, line_list: list) -> bool:
        '''
        Проверка на правильность формата строки
        
        Параметры:
        line_list [:list] - список строк
        
        Возвращает:
        bool - результат проверки
        '''
        flag_types = ['<=', '=>', '->', '**', '==']
        if line_list[3] not in flag_types:
            return False
        elif '@' not in line_list[4]:
            return False
        else:
            return True
        
    def prepare_message(self, line_list: list) -> dict:
        '''
        Подготовка сообщения
        
        Параметры:
        line_list [:list] - список строк
        
        Возвращает:
        message [:dict] - словарь данных
        '''
        created_date, created_time, int_id, flag, address, *other = line_list
        created = datetime.datetime.strptime(f'{created_date} {created_time}', '%Y-%m-%d %H:%M:%S')
        message = {
            'created': created,
            'id': line_list[-1].split('=')[1],
            'int_id': int_id,
            'str': f'{int_id} {flag} {address} {" ".join(other)}',
        }
        return message
    
    def prepare_log(self, line_list: list) -> dict:
        '''
        Подготовка лога
        
        Параметры:
        line_list [:list] - список строк
        
        Возвращает:
        log [:dict] - словарь данных
        '''
        created_date, created_time, int_id, flag, address, *other = line_list
        created = datetime.datetime.strptime(f'{created_date} {created_time}', '%Y-%m-%d %H:%M:%S')
        log = {
            'created': created,
            'int_id': int_id,
            'str': f'{int_id} {flag} {address} {" ".join(other)}',
            'address': address
        }
        return log
    
    def prepare_non_format(self, line_list: list) -> dict:
        '''
        Подготовка не правильной по формату строки
        
        Параметры:
        line_list [:list] - список строк
        
        Возвращает:
        non_format [:dict] - словарь данных
        '''
        created_date, created_time, int_id, *other = line_list
        created = datetime.datetime.strptime(f'{created_date} {created_time}', '%Y-%m-%d %H:%M:%S')
        non_format = {
            'created': created,
            'int_id': int_id,
            'str': f'{int_id} {" ".join(other)}'
        }
        return non_format
    
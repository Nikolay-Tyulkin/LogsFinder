import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.core.config import Settings
from app.db.base import engine, Base, get_db
from app.services.log_loader import LogLoader

logging.basicConfig(level=logging.INFO)
settings = Settings()

app = FastAPI(title=settings.API_TITLE, version=settings.API_VERSION, description=settings.API_DESCRIPTION)

# Настройка CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def check_db_connection(max_attempts: int = 10, delay: int = 5):
    """Ожидает подключения к базе данных перед инициализацией."""
    attempt = 0
    while attempt < max_attempts:
        try:
            # Пробуем подключиться к базе данных
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logging.info("Установлено соединение с базой данных.")
            return
        except Exception as e:
            attempt += 1
            logging.warning(f"Не удалось подключиться к базе данных (попытка {attempt}/{max_attempts}): {e}")
            await asyncio.sleep(delay)
    logging.error("Не удалось подключиться к базе данных после нескольких попыток.")
    raise ConnectionError("PostgreSQL не запущен или недоступен")

async def init_db():
    '''
    Процедура инициализации базы данных
    '''
    await check_db_connection() 
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logging.info("Database tables created")
    
    async for session in get_db():
        async with session.begin():
            log_loader = LogLoader(settings.TEST_LOG_PATH, session)
            await log_loader.load_logs()

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.get("/")
def read_root():
    return {"message": "Welcome to the IoT VPN Manager API"}
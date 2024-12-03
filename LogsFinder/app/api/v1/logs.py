from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import logging

from app.services.log_service import LogService
from app.schemas.log import LogResponse
from app.db.base import get_db
from app.core.config import settings

router = APIRouter()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.get("/logs/{adress}", response_model=List[LogResponse])
async def get_logs_by_adress(adress: str, limit: int = 100, db: AsyncSession = Depends(get_db)):
    '''
    Функция получения логов по адресу

    Параметры:
    adress: str - адрес для поиска логов
    limit: int - количество логов
    '''
    log_service = LogService(db)
    logging.info(f"Getting logs for adress: {adress}")
    return await log_service.get_logs_by_adress(adress, limit)

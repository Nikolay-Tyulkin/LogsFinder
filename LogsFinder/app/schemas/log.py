from pydantic import BaseModel, Field
from datetime import datetime



class LogResponse(BaseModel):
    '''
    Схема для лога
    '''
    id: int = Field(..., 
                    description="ID лога",
                    example=1)
    logs_entry: str = Field(...,
                            description="Текст лога",
                            example="Log entry")
    timestamp: datetime = Field(...,
                                description="Временная метка",
                                example="2021-10-01T00:00:00")
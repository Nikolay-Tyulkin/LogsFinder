from pydantic import BaseModel, Field
from datetime import datetime



class LogResponse(BaseModel):
    '''
    Схема для лога
    '''
    int_id: str = Field(..., 
                    description="Внутренний ID лога",
                    example="Rwtd6-0000Ac-KA")
    log_entry: str = Field(...,
                            description="Текст лога",
                            example="1Rwtd6-0000Ac-Lo == grereyjbpddf@gmail.com R=dnslookup T=remote_smtp defer (-1): domain matches queue_smtp_domains, or -odqs set")
    timestamp: datetime = Field(...,
                                description="Временная метка",
                                example="2021-10-01T00:00:00")
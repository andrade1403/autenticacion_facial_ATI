import uuid
from typing import List
from datetime import datetime
from pydantic import BaseModel, Field

class FaceRegistration(BaseModel):
    id: str = Field(default_factory = lambda: str(uuid.uuid4()))
    userId: str
    embeddingVector: List[float] = Field(default_factory = list)
    fechaRegistro: datetime = Field(default_factory = datetime.utcnow)
import uuid
from typing import List
from pydantic import BaseModel, Field
from datetime import datetime, timezone

class FaceRegistration(BaseModel):
    id: str = Field(default_factory = lambda: str(uuid.uuid4()))
    userId: str
    embeddingVector: List[float] = Field(default_factory = list)
    fechaRegistro: datetime = Field(default_factory = datetime.utcnow)
import uuid
from datetime import datetime
from pydantic import BaseModel, Field

class LogIn(BaseModel):
    id: str = Field(default_factory = lambda: str(uuid.uuid4()))
    userId: str
    fechaLogIn: datetime = Field(default_factory = datetime.utcnow)
    resultado: bool = True
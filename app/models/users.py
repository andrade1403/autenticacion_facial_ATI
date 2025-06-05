import uuid
from pydantic import BaseModel, Field

class User(BaseModel):
    id: str = Field(default_factory = lambda: str(uuid.uuid4()), alias = "userId")
    name: str
    email: str

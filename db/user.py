from pydantic import BaseModel


class User(BaseModel):
    id: str
    username: str
    full_name: str
    email: str
    

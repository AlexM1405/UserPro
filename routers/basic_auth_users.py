from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disable:bool

class UserDB(User):
    id: int
    password:str

user_db = [
     { "id": "1",
       "username": "johndoe", 
       "full_name": "John Doe", 
       "email": "john@example", 
       "password": "pass124" ,
       "disable": "true"
    },
     { "id": "2",
       "username": "Alexm", 
       "full_name": "Alex Mora", 
       "email": "AlexM@example", 
       "password": "Alex1345" ,
       "disable": "false"
    },
     { "id": "3",
       "username": "jamesBon", 
       "full_name": "James Bond", 
       "email": "jamesBond@example", 
       "password": "654321" ,
       "disable": "false"
    }
]

def search_user(username: str):
    if username in user_db:
        return UserDB(**user_db[username])
    
async def current_user(token: str = Depends(oauth2_scheme)):
    user = search_user(token)
    if not user:
        raise HTTPException(
         status_code=401,
         detail='Invalid token',
         headers={"WWW-Authenricate" : "Bearer"})
    
    if user.disable:
        raise HTTPException(
         status_code=400,
         detail='This account has been disabled',)
    return user
    

@router.post("/login")
async def login(form_data : OAuth2PasswordRequestForm = Depends()):
    user = search_user.__get__(form_data.username)
    if not user_db:
        raise HTTPException(status_code=401, detail="Incorrect username")
    
    user = search_user(form_data.password)
    if form_data.password == user.password:
        raise HTTPException(
            status_code=401, detail="Incorrect password")
    
    return {"access_token": user.username, "token_type": "bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET_KEY = "ADJKGIWEHTIAUTHAGERIOJAHGEKTPOIAGET"

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

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
       "password": "$2a$12$Wa7BeAkcxsjLOOfVBWoyr.T3lGheYM58rIRHl2S7X5wlFgdwFUDFS" ,
       "disable": "true"
    },
     { "id": "2",
       "username": "Alexm", 
       "full_name": "Alex Mora", 
       "email": "AlexM@example", 
       "password": "$2a$12$a5Y5tWbpFKGhzRisWMeASuwKYYHhiff5XtHOXkkvmiJalGf7w7SJC" ,
       "disable": "false"
    },
     { "id": "3",
       "username": "jamesBon", 
       "full_name": "James Bond", 
       "email": "jamesBond@example", 
       "password": "$2a$12$4DqwuiQtzk0tPGrBkDcvROtwGTIUpNnnOM4VoFjaAmXlqBMDghQNm" ,
       "disable": "false"
    }
]

def search_user(username: str):
    if username in user_db:
        return UserDB(**user_db[username])
    
async def auth_user(token: str = Depends(oauth2_scheme)):

    try:
        username = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Invalid token')
        
    except JWTError:
        raise HTTPException(
         status_code=status.HTTP_401_UNAUTHORIZED,
         detail='Invalid token',
         headers={"WWW-Authenricate" : "Bearer"})
    return search_user(username)
    
async def current_user(user: User = Depends(auth_user)):
    if user.disable:
        raise HTTPException(
         status_code=status.HTTP_400_BAD_REQUEST,
         detail='This account has been disabled',)
    return user
    

@router.post("/login")
async def login(form_data : OAuth2PasswordRequestForm = Depends()):
    user = search_user.__get__(form_data.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username")
    
    user = search_user(form_data.password)

    if not crypt.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")
    
    
    access_token = {"sub": user.username,
                     "exp":datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)}

    
    return {"access_token": jwt.encode(access_token, SECRET_KEY ,algorithm=ALGORITHM) , "token_type": "bearer"}

    
@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/users",
                   responses={404: {"message": "Dont found it"}})

class User(BaseModel):
    name: str
    surname: str
    position: str
    age: int

users_List = [
    { "id": "1",
      "name": "John",
      "surname": "Doe",
      "position": "Software Engineer",
      "age": 30
    },
    { "id": "2",
      "name": "Jane",
      "surname": "Smith",
      "position": "Product Manager",
      "age": 35
    }
  ]


@router.get("/users")
async def root():
    return {"Hello": "Users"}



@router.get("/users")
async def users():
    return users_List

@router.get("/users/{id}")
async def user(id:int):
   return search_user(id)

@router.get("/")
async def user(id:int):
   return search_user(id)
    

def search_user(id:int):
    users = filter(lambda user: user.id == id, users_List)
    try:
        return list(users)[0]
    except:
        return {"Error": "User Dont find"}
    

@router.post("/user/")
async def create_user(user: User):
    if type(search_user(user.id)) == User:
         return {"Error": "User Exist"}
    else:
        users_List.append(user)

@router.put("/user/")
async def update_user(user: User):

    found = False 

    for index, saved_user in enumerate(users_List):
        if saved_user['id'] == user.id:
            users_List[index] = user
            found = True
    if not found:
     return {'error': 'User Not Found'}

@router.delete("/user/")
async def delete_user(id: int):
    for index, saved_user in enumerate(users_List):
        if saved_user['id'] == id:
            del users_List[index]


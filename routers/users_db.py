from fastapi import APIRouter, HTTPException, status
from db.user import User
from db.client import db_client
from db.schemas.user import user_schema, users_schema
from bson import ObjectId

router = APIRouter(prefix="/usersdb",
                    tags=["usersdb"],
                    responses={status.HTTP_404_NOT_FOUND: {"message": "Dont found it"}})


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

@router.get("/", response_model=list[User])
async def users():
    return db_client.local.users.find()

@router.get("/{id}")
async def user(id: str):
   return search_user("_id", ObjectId(id))
    
@router.get("/")
async def user(id: str):
   return search_user("_id", ObjectId(id))
    

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    if type(search_user_by_email(user.email)) == User:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already in use.")
    
    user_dict = dict(user)
    del user_dict["id"]

    id = db_client.local,users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.local.users.find_one({"id": id}))
    return User(**new_user)

@router.put("/", response_model=User)
async def update_user(user: User):

    user_dict = dict(user)
    del user_dict["id"]

    try:
        db_client.local.users.find_one_and_replace(
            {"_id": ObjectId(user.id)}, user_dict)
    except:
     return {'error': 'User Not Found'}
    
    return search_user("_id", ObjectId(user.id))

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str):
    
    found = db_client.local.users.find_one_and_delete({"_id": ObjectId(id)})
        
    if not found:
     return {'error': 'User Not Found'}

def search_user_by_email(email: str):

    try:
          user = db_client.local.users.find_one({"email": email})
          return User(**user_schema(user))
    except:
       return {"Erro": "User Not Found"}

def search_user(field: str, key:str):
    
    try:
        user = db_client.local.users.find_one({field:key})
        return User(**users_schema(user))
    except:
        return {"Error": "User Not Found"}
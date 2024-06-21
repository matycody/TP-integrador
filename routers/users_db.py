from fastapi import APIRouter, HTTPException,status
from db.models.user import User
from db.client import db_client
from db.schemas.user import user_schema, users_schema
from bson import ObjectId

router = APIRouter(prefix="/userdb",
                   tags=["/userdb"],
                   responses={404: {"message": "No encontrado"}})

users_list= []

#7
@router.get("/", response_model= list[User])
async def users():
    return users_schema(db_client.users.find())

# PATH
@router.get("/{id}")
async def user(id: str):
    return (search_user("_id",ObjectId(id)))
 
# QUERY

@router.get("/")
async def user(id: str):
    return (search_user("_id",ObjectId(id)))

@router.post("/",response_model=User,status_code=status.HTTP_201_CREATED) 
async def user(user:User):
    if type(search_user("email", user.email)) == User:
        raise HTTPException(status_code=404, detail="El usuario ya existe")
    
    #1 inserta el usuario
    user_dict = dict(user)
    #3 el id se encarga el mongodb de genrarlo
    del user_dict["id"]
    #2 guarada el usuario
    id = db_client.users.insert_one(user_dict).inserted_id
    
    #4 criterio de busqueda: q me busque id en la base de datos
    new_user = user_schema(db_client.users.find_one({"_id":id}))
    #5 retorna user 
    
    return User(**new_user)
   
    


@router.put("/",response_model=User)
async def user(user:User):
    
    try:
        user_dict = dict(user)
        del user_dict["id"]
        
        db_client.users.find_one_and_replace(
            {"_id":ObjectId(user.id)}, user_dict)
    except:
        return {"error": "No se ha actualizado el usuario"}
    return search_user("_id",ObjectId(user.id))

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id:str):
    
    found = db_client.users.find_one_and_delete({"_id":ObjectId(id)})     
    
    if not found:
        return {"error": "No se ha eliminado el usuario"}

#esta funcion nos permite si este usuario existe de alguna manera

def search_user(field: str,key):
    try:
        user = db_client.users.find_one({field:key})
        return User(**user_schema(user))
    except:
        return {"error": "No se ha encontrado el usuario"}
#     
# 

from fastapi import APIRouter, HTTPException,status
from db.models.user import User
from db.client import db_client #1 
from db.schemas.user import user_schema, users_schema #2
from bson import ObjectId #3

#4
router = APIRouter(prefix="/userdb",
                   tags=["/userdb"],
                   responses={404: {"message": "No encontrado"}})



#Endpoint para Obtener Todos los Usuarios
@router.get("/", response_model= list[User]) #5
async def users(): #6 
    return users_schema(db_client.users.find()) #7

# Endpoint para Obtener un Usuario por ID (Path)
@router.get("/{id}") #8
async def user(id: str): #9
    return (search_user("_id",ObjectId(id))) #10
 
# Endpoint para Obtener un Usuario por ID (Query)
@router.get("/") #11
async def user(id: str): #9
    return (search_user("_id",ObjectId(id))) #10 

#Metodo Post
@router.post("/",response_model=User,status_code=status.HTTP_201_CREATED) 
async def user(user:User): #12
    if type(search_user("email", user.email)) == User: #13
        raise HTTPException(status_code=404, detail="El usuario ya existe")
    user_dict = dict(user) #14
    del user_dict["id"] #15
    id = db_client.users.insert_one(user_dict).inserted_id #16
    new_user = user_schema(db_client.users.find_one({"_id":id})) #17
    return User(**new_user) #18
   
#Metodo Put
@router.put("/",response_model=User)
async def user(user:User): #19
    try:
        user_dict = dict(user) #20
        del user_dict["id"] #21
        db_client.users.find_one_and_replace( {"_id":ObjectId(user.id)}, user_dict) #22
    except:
        return {"error": "No se ha actualizado el usuario"}
    return search_user("_id",ObjectId(user.id)) #23

#Metodo Post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id:str): #24
    found = db_client.users.find_one_and_delete({"_id":ObjectId(id)})#25 
    if not found: #26
        return {"error": "No se ha eliminado el usuario"}

# Función para Buscar Usuarios
def search_user(field: str,key): #27
    try:
        user = db_client.users.find_one({field:key}) #28
        return User(**user_schema(user)) #29
    except: #30
        return {"error": "No se ha encontrado el usuario"}

"""
#1 Importa el cliente de la base de datos.
#2 Importamos los esquemas
#3 Importa ObjectId de BSON para manejar identificadores de documentos en MongoDB.
#4 Crea una instancia de APIRouter con un prefijo y etiquetas para organizar las rutas relacionadas con los usuarios en la base de datos.
#5 Define una ruta GET en "/userdb/" que devuelve una lista de usuarios.
#6 Define una función asíncrona para manejar la solicitud.
#7 Devuelve todos los usuarios de la base de datos, serializados utilizando users_schema.
#8 Define una ruta GET en "/userdb/{id}" que devuelve un usuario por su ID.
#9 Define una función asíncrona para manejar la solicitud
#10 Busca y devuelve el usuario con el ID especificado, utilizando search_user.
#11 Define una ruta GET en "/userdb/" que acepta un parámetro de consulta (query) id.
#12 Define una función asíncrona para manejar la solicitud.
#13 Verifica si el usuario ya existe por su correo electrónico.
#14 Convierte el objeto User en un diccionario.
#15 Elimina el campo id ya que MongoDB generará uno automáticamente.
#16 Inserta el nuevo usuario en la base de datos y obtiene el ID insertado.
#17 Busca y serializa el nuevo usuario.
#18 Devuelve el nuevo usuario como un objeto User.
#19 Define una función asíncrona para manejar la solicitud.
#20 Convierte el objeto User en un diccionario.
#21 Elimina el campo id.
#22 Reemplaza el usuario en la base de datos.
#23 Devuelve el usuario actualizado.
#24 Define una función asíncrona para manejar la solicitud.
#25 Elimina el usuario de la base de datos.
#26 Si el usuario no se encuentra, devuelve un mensaje de error.
#27 Define una función para buscar usuarios en la base de datos.
#28 Busca un usuario en la base de datos por un campo específico.
#29 Devuelve el usuario encontrado como un objeto User.
#30 Maneja cualquier excepción.
"""
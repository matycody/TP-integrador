from fastapi import APIRouter, HTTPException
from pydantic import BaseModel #1 
from typing import Optional #2 


router = APIRouter()

#3
class User(BaseModel):
    id: Optional[int]
    username: str
    email: str
    
#4    
users_list= []

#Obtener Todos los Usuarios
@router.get("/users")
async def users():
    return users_list

# Obtener Usuario por ID (Path Parameter)
@router.get("/user/{id}") 
async def user(id: int):
    return search_user(id)

# Obtener Usuario por ID (Query Parameter)
@router.get("/user/")  
async def user(id: int):
    return search_user(id)

#Metodo Post
@router.post("/user/", response_model=User, status_code=201) 
async def user(user: User): #5 
    users_list.append(user) #6 
    if type(search_user(user.id)) == User: #7 
        raise HTTPException(status_code=400, detail="El usuario ya existe") #8 
    return user #9 

#Metodo Put
@router.put("/user/")   
async def user(user: User):#5
    found = False #10 
    for index, saved_user in enumerate(users_list): #11  
        if saved_user.id == user.id: #12 
            users_list[index] = user #13 
            found = True #14 
    if not found: #15 
        return {"error": "No se ha actualizado el usuario"} 
    return user #16 

#Metodo Delete
@router.delete("/user/{id}")
async def user(id: int):
    found = False #10 
    for index, saved_user in enumerate(users_list): #11 
        if saved_user.id == id: #12 
            del users_list[index] #17 
            found = True #14
    if not found: #15 
        return {"error": "No se ha eliminado el usuario"} 
    
#Metodo de busqueda por id    
def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list) #18 
    try:
        return list(users)[0] #19 
    except:
        return {"error": "No se ha encontrado el usuario"}

"""
#1- Utilizado para la validación de datos. BaseModel es la clase base para definir modelos de datos.
#2- Indica que un campo puede ser opcional.
#3- Modelo que representa un usuario con tres campos: id, username y email. El campo id es opcional.
#4- Lista que almacenará los usuarios en memoria.
#5- Define una función asíncrona llamada user que acepta un parámetro de tipo User.
#6- Si el usuario no existe, se añade el nuevo usuario a la lista users_list.
#7- Llama a la función search_user con el id del usuario que se intenta crear para verificar si ya existe en users_list.
#8- Si el usuario ya existe, lanza una excepción HTTP con código 404 y un mensaje indicando que el usuario ya existe.
#9- Devuelve el usuario recién creado.
#10- Inicializa una variable booleana found en False. Esta variable se utilizará para indicar si se ha encontrado y actualizado el usuario. 
#11- Itera sobre users_list, proporcionando tanto el índice como el usuario guardado (saved_user).
#12- Comprueba si el id del usuario guardado coincide con el id del usuario proporcionado en la solicitud.
#13- Si se encuentra una coincidencia, actualiza el usuario en users_list en la posición index con el nuevo usuario (user).
#14- Establece found en True para indicar que se ha encontrado/elimiando el usuario.
#15- Verifica si found sigue siendo False después del bucle, lo que indica que no se ha encontrado ningún usuario con el id proporcionado.
#16- Devuelve el usuario actualizado.
#17- Si se encuentra una coincidencia, elimina el usuario de users_list en la posición index.
#18- Filtra users_list para encontrar usuarios cuyo id coincida con el id proporcionado. 
#19- Si es verdad, Convierte el iterador users en una lista y devuelve el primer elemento.
#20- si es falso, retorna un msj de error
"""
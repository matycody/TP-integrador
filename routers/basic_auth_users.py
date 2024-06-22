from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm #1

router = APIRouter()

#2
oauth2 = OAuth2PasswordBearer(tokenUrl="login") 

#Modelos de Datos
class User(BaseModel):
    username: str
    email: str
    disabled: bool
    
class UserDB(User):
    password: str

#Base de datos simulada
users_db = {
    "matias": {
        "username": "matias",
        "email": "matiassosa@gmail.com",
        "disabled": False,
        "password": "123456"
    },
    "nahuel": {
        "username": "nahuel",
        "email": "nahuelparadiso@gmail.com",
        "disabled": False,
        "password": "654321"
    }
}

#Funciones para Buscar Usuarios
#3
def search_user_db(username: str): 
    if username in users_db:
        return UserDB(**users_db[username])

#4
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

# Función para Obtener el Usuario Actual
async def current_user(token: str = Depends(oauth2)): #5
    user = search_user(token) #6
    if not user: #7
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de autenticación inválidas",
            headers={"WWW-Authenticate": "Bearer"})

    if user.disabled: #8
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")

    return user #9 

#Metodo Post
@router.post("/loginbasic") 
async def login(form: OAuth2PasswordRequestForm = Depends()): #10
    user_db = users_db.get(form.username) #11 
    if not user_db: #12
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")

    user = search_user_db(form.username) #13
    if not form.password == user.password: #14
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")

    return {"access_token": user.username, "token_type": "bearer"} #15

# Endpoint para Obtener Información del Usuario Actual
@router.get("/users/me/basic") 
async def me(user: User = Depends(current_user)): #16
    return user #17

"""
#1 Importa las clases necesarias para manejar la autenticación basada en OAuth2.
#2 Configura el flujo de autenticación OAuth2 con la URL del token especificada como "login".
#3 Busca un usuario en users_db y devuelve un objeto UserDB si se encuentra.
#4 Busca un usuario en users_db y devuelve un objeto User si se encuentra.
#5 Define una función asíncrona que depende de oauth2 para obtener el token.
#6 Busca el usuario utilizando el token.
#7 Si el usuario no se encuentra, lanza una excepción HTTP 401 (Unauthorized).
#8 Si el usuario está deshabilitado, lanza una excepción HTTP 400 (Bad Request).
#9 Devuelve el usuario si se encuentra y no está deshabilitado.
#10 Define una función asíncrona para manejar el inicio de sesión, utilizando OAuth2PasswordRequestForm para obtener los datos del formulario.
#11 Busca el usuario en users_db.
#12 Si el usuario no se encuentra, lanza una excepción HTTP 400 (Bad Request).
#13 Busca el usuario en la base de datos.
#14 Si la contraseña no coincide, lanza una excepción HTTP 400 (Bad Request).
#15 Devuelve un token de acceso y el tipo de token.
#16 Define una función asíncrona para manejar la solicitud, dependiendo de current_user para obtener el usuario actual.
#17 Devuelve la información del usuario actual.
"""
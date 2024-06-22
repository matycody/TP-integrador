from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError #1
from passlib.context import CryptContext #2
from datetime import datetime, timedelta #3

router = APIRouter()


ALGORITHM = "HS256" # Define el algoritmo de codificación JWT.
ACCESS_TOKEN_DURATION = 1 # Define la duración del token de acceso en minutos.
SECRET = "201d573bd7d1344d3a3bfce1550b69102fd11be3db6d379508b6cccc58ea230b" # Define la clave secreta utilizada para codificar y decodificar JWTs.

#4
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

#5
crypt = CryptContext(schemes=["bcrypt"]) 

#Modelos de Datos
class User(BaseModel):
    username: str
    email: str
    disabled: bool
    
class UserDB(User):
    password: str


# Base de Datos Simulada de Usuarios
users_db = {
    "matias": {
        "username": "matias",
        "email": "matiassosa@gmail.com",
        "disabled": False,
        "password": "$2a$12$B2Gq.Dps1WYf2t57eiIKjO4DXC3IUMUXISJF62bSRiFfqMdOI2Xa6" #123456
    },
    "nahuel": {
        "username": "nahuel",
        "email": "nahuelparadiso@gmail.com",
        "disabled": False,
        "password": "$2a$12$LQa/B8gDx0gIch2tCfatqOnPDxZpMZgpnkypF1ZAfsu5poQHWkprC" #nahuel12 
    }
}

# Funciones para Buscar Usuarios

def search_user_db(username: str): #6
    if username in users_db:
        return UserDB(**users_db[username])


def search_user(username: str): #7
    if username in users_db:
        return User(**users_db[username])
    
#Función para Autenticar el Usuario
async def auth_user(token: str = Depends(oauth2)): #8
    exception = HTTPException( #9
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de autenticación inválidas",
        headers={"WWW-Authenticate": "Bearer"})
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub") #10
        if username is None: #11
            raise exception
    except JWTError: #12 
        raise exception
    return search_user(username) #13

# Función para Obtener el Usuario Actual
async def current_user(user: User = Depends(auth_user)):
    if user.disabled: #14
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")
    return user #15
    
   
# Metodo Post
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()): #16
    user_db = users_db.get(form.username) #17 
    if not user_db: #18 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    user = search_user_db(form.username) #19 
    if not crypt.verify(form.password, user.password): #20 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    #21    
    access_token = {"sub": user.username,
                    "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)}
    
    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"} #22


# Endpoint para Obtener Información del Usuario Actual
@router.get("/users/me")
async def me(user: User = Depends(current_user)): #23
    return user #24

"""
#1 Importa funciones para codificar y decodificar JWTs.
#2 Importa funciones para manejar el hashing de contraseñas.
#3 Importa clases para manejar fechas y tiempos.
#4 Configura el flujo de autenticación OAuth2 con la URL del token especificada como "login".
#5 Configura el contexto de hashing de contraseñas con el esquema bcrypt.
#6 Busca un usuario en users_db y devuelve un objeto UserDB si se encuentra.
#7 Busca un usuario en users_db y devuelve un objeto User si se encuentra.
#8 Define una función asíncrona que depende de oauth2 para obtener el token.
#9 Define una excepción HTTP 401 (Unauthorized) para usar en caso de errores de autenticación.
#10 Decodifica el token JWT y obtiene el nombre de usuario (sub).
#11 Si el nombre de usuario no está en el token, lanza la excepción.
#12 Captura cualquier error relacionado con JWT y lanza la excepción.
#13 Devuelve el usuario encontrado.
#14 Si el usuario está deshabilitado, lanza una excepción HTTP 400 (Bad Request).
#15 Devuelve el usuario si no está deshabilitado.
#16 Define una función asíncrona para manejar el inicio de sesión, utilizando OAuth2PasswordRequestForm para obtener los datos del formulario.
#17 Busca el usuario en users_db.
#18 Si el usuario no se encuentra, lanza una excepción HTTP 400 (Bad Request).
#19 Busca el usuario en la base de datos.
#20 Si la contraseña no coincide, lanza una excepción HTTP 400 (Bad Request).
#21 Crea un diccionario con los datos del token, incluyendo el nombre de usuario (sub) y la fecha de expiración (exp).
#22 Devuelve un token de acceso y el tipo de token (Bearer).
#23 Define una función asíncrona para manejar la solicitud, dependiendo de current_user para obtener el usuario actual.
#24 Devuelve la información del usuario actual.
"""






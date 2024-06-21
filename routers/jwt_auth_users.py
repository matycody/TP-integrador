from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError#1
from passlib.context import CryptContext#2 ->
from datetime import datetime, timedelta#3
2#
router = APIRouter()
#11
ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1 #7
SECRET = "201d573bd7d1344d3a3bfce1550b69102fd11be3db6d379508b6cccc58ea230b" 

4#
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"]) #11 contexto de importacion ->
3#
class User(BaseModel):
    username: str
    email: str
    disabled: bool


class UserDB(User):
    password: str


5#
users_db = {
    "matias": {
        "username": "matias",
        "email": "matiassosa@gmail.com",
        "disabled": False,
        "password": "$2a$12$B2Gq.Dps1WYf2t57eiIKjO4DXC3IUMUXISJF62bSRiFfqMdOI2Xa6" #openssl para encriptar la contraseña
    },
    "nahuel": {
        "username": "nahuel",
        "email": "nahuelparadiso@gmail.com",
        "disabled": False,
        "password": "$2a$12$LQa/B8gDx0gIch2tCfatqOnPDxZpMZgpnkypF1ZAfsu5poQHWkprC" #nahuel12 openssl para encriptar la contraseña
    }
}
# 6
def search_user_db(username: str): 
    if username in users_db:
        return UserDB(**users_db[username])


def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    
#10
async def auth_user(token: str = Depends(oauth2)):

    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de autenticación inválidas",
        headers={"WWW-Authenticate": "Bearer"})

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception

    except JWTError:
        raise exception

    return search_user(username)

#9
async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")

    return user    
    
#7    
#primero importamos el post de basic
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()): #Se reciben las credenciales del usuario a través del formulario OAuth2PasswordRequestForm, que incluye el nombre de usuario y la contraseña.

    user_db = users_db.get(form.username) # Se busca el usuario en la base de datos simulada users_db. Si el usuario no existe, se lanza una excepción HTTP con un mensaje de error.
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")

    user = search_user_db(form.username) #Se verifica que la contraseña proporcionada coincida con la contraseña encriptada almacenada. Si no coincide, se lanza una excepción HTTP con un mensaje de error.
    #8
    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    
    #9 duracion del token # Se crea un diccionario con los datos del token, incluyendo el nombre de usuario (sub) y la fecha de expiración (exp).
    access_token = {"sub": user.username,
                    "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)}
    #10 devuelve el SECRET -= # Se codifica el token usando jwt.encode con una clave secreta y el algoritmo especificado. Finalmente, se devuelve el token de acceso y el tipo de token (Bearer) al cliente.
    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}    



@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user

# # python -m uvicorn jwt_auth_users:router --reload 
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()
#2
oauth2 = OAuth2PasswordBearer(tokenUrl="login")
#-1
class User(BaseModel):
    username: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

#0
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
#4
def search_user_db(username: str): 
    if username in users_db:
        return UserDB(**users_db[username])


def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

#5
async def current_user(token: str = Depends(oauth2)): #4
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de autenticación inválidas",
            headers={"WWW-Authenticate": "Bearer"})

    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")

    return user

#3
@router.post("/loginbasic") #2
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")

    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")

    return {"access_token": user.username, "token_type": "bearer"}

@router.get("/users/me/basic") #3
async def me(user: User = Depends(current_user)):
    return user


# python -m uvicorn basic_auth_users:router --reload
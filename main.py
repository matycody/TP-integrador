from fastapi import FastAPI  #1- importamos FastApi
from routers import users, jwt_auth_users, basic_auth_users, users_db


#Routers
app = FastAPI() #2- creamos la instacia FastApi



app.include_router(users.router)
app.include_router(jwt_auth_users.router)
app.include_router(basic_auth_users.router)
app.include_router(users_db.router)




@app.get("/") #3- Define un decorador de operaciones de path
async def root(): #4- define la función de la operación de path
    return {"message": "Hello World"} #5- devuelve el contenido

# python -m uvicorn main:app --reload

@app.get("/url")
async def url():
    return{ "url_curso":"https://tpintegrador@gmail.com"}
# http://127.0.0.1:8000/url


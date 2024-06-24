from fastapi import FastAPI  #1
from routers import users, jwt_auth_users, basic_auth_users, users_db

app = FastAPI() #2

#Routers
app.include_router(users.router)
app.include_router(jwt_auth_users.router)
app.include_router(basic_auth_users.router)
app.include_router(users_db.router)




@app.get("/") #3
async def root(): #4
    return {"message": "Hello World"} #5

@app.get("/url") #3
async def url(): #4
    return{ "url_curso":"https://tpintegrador@gmail.com"} #5

"""
#1- importamos FastApi
#2- creamos la instacia FastApi, sera el principal punto de interaccion para crear toda la FastApi
#3- Define un decorador de operaciones de path, le dice a FastAPI que la funcion de abajo esta a cargo de manejar las solictudes que van a: @app.get("/")
#4- define la función de la operación de path, FastAPI lo llamará cada vez que reciba una solicitud a la URL mediante una operación .get
#5- devuelve el contenido

# arranque del servidor: python -m uvicorn main:app --reload
# dirrecciones de las url: http://127.0.0.1:8000/  y  http://127.0.0.1:8000/url

"""

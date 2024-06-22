# Instalación e Implementación de FastAPI

## Instalación

### 1 - El primer paso es instalar FastAPI y nuestro servidor local Uvicorn(en la terminal con la dirección de nuestro directorio).

```bash
pip install fastapi 
```


```bash
pip install "uvicorn[standard]"
```

#### Utilizaremos un archivo main_py para enrutar todos los archivos de nuestro proyecto 

### 2- Importamos FastAPI y ponemos un codigo de prueba:
```
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/url")
async def url():
    return{ "url":"https://tpintegrador@gmail.com" }
```

### 3- Corremos el servidor en la terminal situado en nuestro directorio mediante uvicorn

Ej:
* ```C:\Users\User\OneDrive\Escritorio\FASTAPI_TP> uvicorn main:app --reload```

** Si tira este error:
"uvicorn" no se reconoce como un comando interno o externo,
programa o archivo por lotes ejecutable.

Utilize esta linea de codigo en la terminal: 

* ```C:\Users\User\OneDrive\Escritorio\FASTAPI_TP>python -m uvicorn main:app --reload```

si el servidor funciono correctamente, en la terminal muestra lo siguiente:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [28720] 
INFO:     Started server process [28722]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Ahora pondremos un ejemplo con la extensión Thunder client(tambien se puede utilizar postgram) para esta prueba 

[Ejemplo de uso ](https://www.youtube.com/watch?v=_XjQP6V-Tfg)

### 4- En nuestro directorio principal, creamos dos carpetas llamadas:
- routers: donde se insertaran nuestros ficheros principales del proyecto
- db: donde irán todos nuestros ficheros relacionados con la base de datos no relacional que utilizaremos 

### Dentro de nuestra carpeta "routers", crearemos 4 archivos .py llamados:
- users.py
- usersdb.py
- basic_auth_users.py
- jwt_auth_users.py

--- 
Cada archivo .py mencionado anteriormente debe estar conectado al fichero main.py con ApiRouter, que es una clase de FastAPI que permite agrupar rutas y organizarlas mejor.

```
from fastapi import ApiRouter

router = ApiRouter()

```
Creamos la instacia ApiRouter, sera el principal punto de interacción para crear y vincular todos los ficheros.
#

### Dentro de nuestra carpeta "db", crearemos 2 carpetas y un archivo .py llamados:
* models
* client

donde cada carpeta tendra un fichero user.py, que explicaremos mas adelante.
Estas carpetas le daran formato e implmentacion  de insercion a nuestra base de datos 

y nuestro fichero:

* client.py

que nos permitira conectarnos mas adelante a nuestra base de datos **local** o mediante una **Conexión Remota con URI de Conexión**

### 5- Enrutamos los archivos dentro de nuestra carpeta ***routers*** al main.py mediante una funcion que viene dentro de las funciones de FasApi

```
from fastapi import FastAPI
from routers import users, jwt_auth_users, <-basic_auth_users, users_db <-

app = FastAPI()

app.include_router(users.router) <-
app.include_router(jwt_auth_users.router) <-
app.include_router(basic_auth_users.router) <-
app.include_router(users_db.router)  <- 

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/url")
async def url():
    return{ "url":"https://tpintegrador@gmail.com" }
```
### 6- Empezamos a utilizar el fichero users.py para dar una introduccion a las operaciones basicas de uso de FastApi:

 

<span style="color:green">__get:__</span> para leer datos de usuario

<span style="color:green">__post:__</span> para crear el usuario

<span style="color:green">__put:__</span> para actualizar datos de usuario

<span style="color:green">__delete:__</span> para eliminar el usuario


### Dentro de este fichero __users.py__ importamos :

```
from fastapi import FastAPI, HTTPException <- 3
from pydantic import BaseModel <- 1
from typing import Optional <- 2

router = ApiRouter()

class User(BaseModel):
    id: Optional[int]
    username: str
    email: str
    
users_list= []

@router.get("/users")
async def users():
    return users_list

# Obtener Usuario por ID (Path Parameter) <- 4
@router.get("/user/{id}") 
async def user(id: int):
    return search_user(id)

# Obtener Usuario por ID (Query Parameter) <- 5
@router.get("/user/")  
async def user(id: int):
    return search_user(id)

... 
```

* 1 - Pydantic es una biblioteca de Python que permite la validación y configuración de datos mediante el uso de clases. Al importar su BaseModel, podemos definir atributos y validarlos automáticamente.

* 2- La biblioteca typing de Python proporciona herramientas para indicar tipos de datos de manera estática. Esto es útil para mejorar la claridad del código y para herramientas de análisis estático de código.
Optional es una clase dentro de la biblioteca typing que indica que un valor puede ser del tipo especificado o None.

* 3 - es una clase que se utiliza para generar errores HTTP personalizados y devolver respuestas de error específicas al cliente. Esta excepción se lanza para indicar que algo salió mal en el procesamiento de una solicitud y permite especificar el código de estado HTTP y un mensaje de detalle.

-- -- -- 

Diferencia entre PATH y QUERY:

* 4 - Obtiene un usuario específico basado en el id pasado como parámetro en la URL.(Path)

* 5 - Obtiene un usuario específico basado en el id pasado como parámetro de consulta (Query ).

Por ultimo, Activamos el servidor uvicorn

```C:\Users\User\OneDrive\Escritorio\FASTAPI_TP> uvicorn main:app --reload```

AHORA LE MOSTRAREMOS MEDIANTE UN VIDEO SU EJEMPLO DE USO: 

[Ejemplo de users.py](https://www.youtube.com/watch?v=o69zLHDiUvE)

# Introducimos en este apartado el tema de __security__

### 7- En nuestro fichero __"basic_auth_users.py"__,  utilizaremos FastAPI para crear un sistema de autenticación básico con tokens OAuth2. Los usuarios pueden iniciar sesión y obtener un token de acceso, que luego se utiliza para acceder a rutas protegidas. 

Primeramente, importamos

```
from fastapi import FastAPI
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm 

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    email: str
    disabled: bool



class UserDB(User):
    password: str

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
...

```
Los módulos OAuth2PasswordBearer y OAuth2PasswordRequestForm de la biblioteca fastapi.security son componentes clave para manejar la autenticación basada en OAuth2 en FastAPI.

<span style="color:green">__OAuth2PasswordBearer:__</span>  es una clase que representa un flujo de autenticación OAuth2 donde el cliente necesita obtener un token de acceso mediante un nombre de usuario y una contraseña. Específicamente, esta clase crea un esquema de seguridad para la autenticación de portador con token (Bearer Token Authentication).

<span style="color:green">__OAuth2PasswordRequestForm:__</span> es una clase que facilita el procesamiento de solicitudes de autenticación que utilizan el flujo de "password grant" de OAuth2. Proporciona una forma estándar de obtener los datos del formulario de autenticación (nombre de usuario y contraseña).

<span style="color:yellow">__Depends:__</span>Facilita la inyección de dependencias en FastAPI para reutilizar código y manejar parámetros automáticamente.

<span style="color:yellow">__status:__</span>Proporciona constantes para códigos de estado HTTP, mejorando la legibilidad del código en FastAPI.

### 8- Insertamos los modelos de datos utilizados:

<span style="color:red">__User:__</span> Información visible del usuario.

<span style="color:red">__UserDB:__</span> Extiende User e incluye la contraseña.

Nuestro diccionario <span style="color:red">__users_db__</span> simula una base de datos de usuarios con claves únicas por nombre de usuario. Cada entrada contiene detalles como nombre completo, correo electrónico, estado de activación y contraseña en formato de diccionario interno. Es utilizado para almacenar y acceder a información de usuarios de manera estructurada en aplicaciones de prueba o prototipos.

### 9 - Creamos los métodos 

__Post__. Este endpoint maneja las solicitudes de inicio de sesión. Recibe los datos del formulario de inicio de sesión a través de OAuth2PasswordRequestForm. Verifica si el usuario existe en users_db. Si el usuario no existe o la contraseña es incorrecta, lanza excepciones HTTP con los mensajes correspondientes. Si la autenticación es exitosa, devuelve un token de acceso y el tipo de token.

__me__. Devuelve la información del usuario autenticado. Utiliza Depends(current_user) para obtener el usuario actual autenticado. Si el usuario es autenticado correctamente, devuelve el objeto user.

__search_user_db__. Toma un nombre de usuario como argumento y busca en un diccionario users_db que actúa como una base de datos de usuarios. Si el nombre de usuario existe en users_db, crea y devuelve una instancia de UserDB con los datos del usuario.

__search_user__. Similar a search_user_db, esta función busca un usuario en users_db y devuelve una instancia de User si el usuario existe.

__current_user__. Se encarga de obtener el usuario actual basado en un token de autenticación. Utiliza Depends(oauth2) para extraer y validar el token. Si el usuario no es encontrado o está inactivo (user.disabled es True), lanza excepciones HTTP con los códigos de error correspondientes. Si todo es correcto, devuelve el objeto user.

### Este sistema de autenticación básico permite que los usuarios inicien sesión y accedan a recursos protegidos mediante tokens de acceso.

### 10- Damos inicio a nuestro uvicorn 

```C:\Users\User\OneDrive\Escritorio\FASTAPI_TP> uvicorn main:app --reload```

[Ejemplo de uso de basic_auth_users.py](https://www.youtube.com/watch?v=zPcqM4X24YI)

# Nos introducimos en esta autentificación mas elaborada 

### 11- Con nuestro fichero "jwt_auth_users" hagamos que la aplicación sea realmente segura, utilizando tokens JWT y hash de contraseñas seguras.

### 12- Primeramente, instalamos en nuestra terminal PyJWT y passlib en nuestra terminal:

```C:\Users\User\OneDrive\Escritorio\FASTAPI_TP> pip install "python-jose[cryptography]" ```

```C:\Users\User\OneDrive\Escritorio\FASTAPI_TP> pip install "passlib[bcrypt]"```



### 13- Importamos las librerias:

```
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError#1
from passlib.context import CryptContext 
from datetime import datetime, timedelta

router = APIRouter()

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1 
SECRET = "201d573bd7d1344d3a3bfce1550b69102fd11be3db6d379508b6cccc58ea230b" 


oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"]) 

class User(BaseModel):
    username: str
    email: str
    disabled: bool


class UserDB(User):
    password: str

...

```

<span style="color:green">__jwt:__</span> La librería jose (JavaScript Object Signing and Encryption) proporciona soporte para la creación, firma y verificación de tokens JWT (JSON Web Tokens). Los tokens JWT son utilizados para autenticar usuarios y transportar información de manera segura entre el cliente y el servidor.
<span style="color:green">__JWTError:__</span>
Esta es una excepción proporcionada por la librería jose. Se lanza cuando hay un error al decodificar o verificar un token JWT, como cuando el token es inválido o ha expirado.

<span style="color:green">__CryptContext:__</span> es parte de la librería passlib, que es una biblioteca de Python para el manejo de contraseñas. Proporciona una interfaz para encriptar, verificar y gestionar contraseñas de manera segura.

<span style="color:green">__datetime:__</span> Esta clase del módulo datetime se utiliza para trabajar con fechas y horas.
<span style="color:green">__timedelta:__</span> se utiliza para representar una duración, la diferencia entre dos fechas u horas.

### 14- Configuramos el algoritmo de encriptación, la duración del token y la clave secreta. También se establece oauth2 para manejar la autenticación basada en contraseñas y crypt para encriptar las contraseñas.

```
ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1 
SECRET = "201d573bd7d1344d3a3bfce1550b69102fd11be3db6d379508b6cccc58ea230b" 


oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"]) 

```
ademas: 

* Se definen dos modelos: User para representar un usuario sin contraseña y UserDB que incluye la contraseña.

 * users_db actúa como una base de datos de usuarios, donde las contraseñas están encriptadas.

### 15 - Utilizamos el mismo diccionario que el de nuestro fichero "basic_auth_users.py", con la diferencia de que nuestras password esta encryptada, mediante el programa BCrypt generator
[Programa utilizado BCrypt](https://bcrypt-generator.com/)

Mismas funciones __search_user_db__ y __search_user__ para este fichero extraidos del fichero "basic_auth_users.py"

Definimos un endpoint de FastAPI para el inicio de sesión de usuarios utilizando el método POST en la ruta __/login__. Este endpoint verifica las credenciales del usuario y, si son correctas, genera y devuelve un token JWT que el usuario puede usar para acceder a recursos protegidos.

Nuestra funcion __me__. Este endpoint devuelve la información del usuario autenticado.

Nuestra funcion __auth_user__ valida el token JWT y extrae el nombre de usuario. Si el token es inválido, lanza una excepción.

La funcion __curent_user__ verifica si el usuario está deshabilitado y, si no lo está, lo devuelve.

### 16 - Reiniciamos el servidor uvicorn en la terminal y verificamos:

```C:\Users\User\OneDrive\Escritorio\FASTAPI_TP> uvicorn main:app --reload```

[Ejemplo de uso de jwt_auth_users.py](https://www.youtube.com/watch?v=QMbzeLhWph4)

# Por ultimo, llevamos a cabo un ejemplo de FastAPI a una base de datos no relacional como MongoDB 

### 17 - Instalación de MongoDB y MongoDB Atlas:

Para windows: 

Visita la página oficial de descargas de MongoDB: MongoDB Download Center.
Selecciona la versión adecuada para Windows y haz clic en "Download".
Ejecutar el instalador:

Ejecuta el archivo .msi descargado.
Sigue las instrucciones del instalador. Asegúrate de seleccionar la opción para instalar MongoDB como un servicio (Service) y configurarlo para que se inicie automáticamente con Windows.
Configurar la variable de entorno:

Añade el directorio bin de MongoDB a la variable de entorno PATH. Por defecto, suele estar en C:\Program Files\MongoDB\Server\<version>\bin.
Abre el Panel de Control, ve a Sistema y Seguridad, Sistema, Configuración avanzada del sistema, y luego Variables de entorno.
En Variables del sistema, selecciona Path y haz clic en Editar. Añade la ruta al directorio bin de MongoDB.
Verificar la instalación:

Abre una nueva ventana de cmd y ejecuta mongod para iniciar el servidor MongoDB.
En otra ventana de cmd, ejecuta mongo para iniciar la shell de MongoDB y conectarte al servidor.

### 18 - Creamos nuestra cuenta en MongoDb Atlas

[Tutorial de INSTALACIÓN para Mongodb y MongodbAtlas](https://www.youtube.com/watch?v=hC1_qA5BAU4) hasta 4:29 

[Documentacion oficial](https://www.mongodb.com/docs/)


### 19 - Suponiendo que esta instalado nuestro Mongodb en nuestro entorno sea virtual o local, utilizaremos nuestro fichero "__users_db.py__" para todo lo relacionado a la inserción de usuarios a la base de datos de MongoDb Atlas

Pero antes, en el fichero "__client.py__", dentro de nuestra carpeta "__db__" importamos:


```
from pymongo import MongoClient

# db_client = MongoClient().local

db_client = MongoClient("mongodb+srv://test:test@cluster0.izci727.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0").test

```

 La clase <span style="color:green">__MongoClient__</span>  de la librería pymongo. MongoClient es la clase principal utilizada para establecer una conexión con un servidor MongoDB.


```db_client = MongoClient(
    "mongodb+srv://test:test@cluster0.izci727.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0").test
```  

#### Establece una conexión a una base de datos MongoDB alojada en MongoDB Atlas, un servicio de base de datos en la nube.

[Tutorial de INSTALACIÓN MongodbAtlas y el contenedor que utilizaremos en nuestro fichero (client.py)](https://www.youtube.com/watch?v=hC1_qA5BAU4) despues de 4:29 

#### 20 - Dentro de nuestra carpeta __"db__" utilizamos un fichero llamado "__user.py__", que en el estara el esquema de nuestra clase User(que luego sera exportada a nuestro fichero "__users_db.py__"). Dentro de esa misma carpeta "__"db__", creamos una subcarpeta llamada "__schemas__", que tambien contendra un archivo "__user.py__", pero a diferencia del anterior __"user.py__", este convierte documentos de MongoDB en un formato que puede ser devuelto por tus endpoints de FastAPI.

## Con esto ya instalado y explicado, comenzamos con el final del proyecto.

### 21 - importamos todos los archivos antes mencionados en la carpeta "__db"__ a nuestro fichero "__usersdb.py__":

```
from fastapi import APIRouter, HTTPException,status
from db.models.user import User
from db.client import db_client
from db.schemas.user import user_schema, users_schema
from bson import ObjectId

router = APIRouter(prefix="/userdb",
                   tags=["/userdb"],
                   responses={404: {"message": "No encontrado"}})

users_list= []

...
```
* <span style="color:green">bson </span> : es una biblioteca utilizada para trabajar con documentos BSON en MongoDB. BSON (Binary JSON) es el formato de almacenamiento utilizado por MongoDB para representar documentos de datos.

### 22 - Modificamos nuestro archivo usado previamente ("__users.py__") para poder insertar usuarios ahora en una base de datos en la nube(MongoDB Atlas)

### 23 - Una vez terminado esto, corremos el servidor uvicorn 

```C:\Users\User\OneDrive\Escritorio\FASTAPI_TP> uvicorn main:app --reload```

[Ejemplo de uso completo para inserción de base de datos](https://www.youtube.com/watch?v=D9ICMDde640)















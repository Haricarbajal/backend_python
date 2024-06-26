from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

"""OAuth2 especifica que al usar el "flujo de contraseña" (que estamos usando)
el cliente/usuario debe enviar campos usernamey passwordcomo datos del formulario.
Y la especificación dice que los campos deben tener ese nombre. Entonces user-nameo emailno funcionaría.

Pero no te preocupes, puedes mostrarlo como desees a tus usuarios finales en el frontend.

Y sus modelos de base de datos pueden usar cualquier otro nombre que desee.
Pero para la operación de ruta de inicio de sesión , necesitamos usar estos nombres para que sean compatibles con la 
especificación (y poder, por ejemplo, usar el sistema de documentación API integrado).
La especificación también establece que usernamey passworddebe enviarse como datos de formulario (por lo tanto, aquí no hay JSON)"""


app = FastAPI()



"""OAuth2PasswordRequestForm:
Primero, importe OAuth2PasswordRequestFormy utilícelo como una dependencia Dependsen la operación de ruta para /login:"""
"""esta se encarga de gestionar la autenticaion, para poder utenticarlo se tiene que llamar a la api con /login
y ella se va a encargar de poder autenticarlo"""
oauth2 = OAuth2PasswordBearer(tokenUrl="login")



class User(BaseModel):
    username : str
    full_name : str
    email : str
    desabled : bool




#UserDB hereda todos los atributos que tiene user(user está definido como modelo base)
"""lo que hace userDB es crear una clase en la que que se encuentran todos los atributos de users y agrega el atributo de password,
no agrega a la clase user, lo que hace es que se crea una nueva clase que tien por nombre user db. Esto sirve pra un mejor manejo de los datos del cliente, especialmente los datos sensibles"""
class UserDB(User):
    password : str


users_db = {
    "user1": {
        "username" : "harics",
        "full_name": "hari carbajal",
        "email": "armandolegos@gmail.com",
        "desabled": False,
        "password": "123456"
    },
    "user2": {
        "username" : "paco",
        "full_name": "hari carbajal",
        "email": "armandolegos@gmail.com",
        "desabled": False,
        "password": "654321"
    }
}



def search_user(username : str):#Lo que espera recibir es una clave de diccionario...ejemplo: "user1"
    if username in users_db:#esta funcion verifica si username(quiere decir "user1"), esta dentro de la lista de diccionario de users_db. En este caso es true porque "user1" si está dentro de users_db
        return UserDB(**users_db[username])#se accede a los valores que se tiene asociado a la clave de "user1"
    
    """La clase UserDB solo tiene el atributo de password, pero al heredar los atributos de User(los campos de username, full_name, email, desabled)...al 
    programar UserDB(users_db[username]) estamos pasando todos los datos o atributos que hemos recogido del diccionario de users_db anteriormente.
    Entonces la clase UserDB herada de User y añade un campo adicional que es password, es aqui donde entra en juego pydantic, pydantic hace una validacion automatica 
    par asegurar que todos los atributos cumplan las especificaciones definidas en la clase de User(BaseModel) y junto con el modelo extendido UserDB"""

async def current_user(token : str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Credenciales de autenticacion invalidas",
                            headers={"www-Authenticate": "Bearer"})
    return user


@app.post("/login")
async def login(formulario : OAuth2PasswordRequestForm = Depends()):
    """formulario es un parametro de la funcion logion por que formulario posria tener cualquier otro nombre, 
    el parametro formulario es de tipo OAuth2PasswordRequestForm, es decir que espera los campos de username y password, entre otros que podemos ver en la documentacion"""


    """En este ejemplo solo vamos a necesitar el username"""
    user_dict = users_db.get(formulario.username)#estamos cogiendo el username que nos ha proporcionado el cliente para verificar que exista en la "base de datos" de users_db, para luego guardarlo en la vairable de user_dict
    if not user_dict:#si no existe user enonces se envia una exception al servidor
        raise HTTPException(status_code=400,
                            detail="El usuario no es correcto")
    #si no se cumple la condicion de arriba entonces significa que el usuario si existe, por lo tanto el programa si con el flujo de ejecucion,
    #sigue con la funcion de abajo

    user = search_user(formulario.username)
    """Una vez se haya comprobado que el usuario si existe, se guarda la instancia que va a generar la funcion search_user con su llamado, le pasaremos como parametro el username que nos proporciona el cliente enel formulario
    , de esta manera tendremos un mejor contro de los campos de este"""
    if not formulario.password == user.password:
        """verificamos que la contraseña del ususario sea la correcta, esto se hace entrando al atibuto password < que nos ha proporcionado el usuario, para luego compararlo
        con la contraseña encontrada con la funcion de search_user(formulario.username) es decir con la variable user... la compracion de la dos contraseñas se varia de esta manera:
        if not formulario.password in user.password: esto quiere decir SI la contraseña de formulario NO es la contraseña de user...ENTONCES..."""
        raise HTTPException(status_code=400, 
                            detail="la contraseña no es coreecta")

    return {"acces_token" : user.username, "token_type" : "bearer"}


@app.get("/users/me")
async def me(user : User = Depends(current_user)):
    return user
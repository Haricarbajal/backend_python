from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

app = APIRouter(prefix="/users",tags=["Users"])

class User(BaseModel):
    id : int
    name : str
    surname : str
    url : str
    age : int

user_list = [User(id=1, name="Brais", surname="Moure", url="https://moure.dev", age=35),
        User(id=2,name="juan", surname="dev", url="https://mouredev.com", age=26),
        User(id=3,name="hari", surname="dahlberg", url="https://haakon.com", age=33)]

@app.get("/json")
async def usersjson():
    return [{"name": "Brais", "surname": "moure", "url":"https://moure.dev", "age": 35},
            {"name": "juan", "surname": "dev", "url": "https://moredev.com", "age": 26},
            {"name": "hari", "surname": "dahlberg", "url": "https://haakon.com", "age": 33}]




@app.get("/")
async def users():
    return user_list



#ejemplo de busqueda por http con el parametro de path: http:localhost/8000/user/1
#especificamos el numero de id por el cual queremos hacer la busqueda http
@app.get("/user/{id}", response_model=User, status_code=200)
async def user(id : int):
    buscar_user = search_user(id)
    if buscar_user is None:
        raise HTTPException(status_code=404, detail="No existe el id de ese usuario")
    
    return buscar_user
"""A continuacion veremos la utilidad de None en la funcion de search_User:
Se guarda la respuesta de la funcion de search_user, tenemos dos posibilidades que lo que devuelva sea el usuario o 
el valor None. Entonces hacemos una condicional en la cual si el valor retornado es None, entonces se ejecuta el raise, ya que entendemos que no existe ese usuario,
por otro lado si el valor NO ES NONE entonces retorna el usuario encontrado"""






#ejemplo de busqueda por http con el parametro de query: http:localhost/8000/?id=1
"""con el ? indicamos que empezaremos a realizar la busqueda por query luego
colocaremos el filtro por el cual queremos realizar la busqueda http y con el signo igual "=" le daremos un valor"""
#se pueden concatenar los "filtros" usando &...ejemplo: http:localhost/8000/?id=1&age=18
@app.get("/userquery/")
async def userquery(id : int):
    buscar_user = search_user(id)
    if buscar_user is None:
        raise HTTPException(status_code=404, detail="El id proporcionado no existe en nigun usuario")
    
    return buscar_user







@app.post("/user/", response_model=User, status_code=201)
async def user(user : User):
    if  type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail="el usuario ya existe")

    user_list.append(user)
    return user

"""El cuerpo que se pasa en el metodo post de este, primero por la validacion del
parametro de user(user : User), esto verifica que se cumpla con la condicion que hemos colocado como modeloBase en User
para luego empezar la funcion, si existe el ide del usuario que hemos pasado, entonces se agrega al user_list y retorna
el user que hemos pasado como parametro, para luego validar esa salida con el response_model=User"""






@app.put("/user/", response_model=User, status_code=201)
async def user(user : User):
    found = False
    for index, saved_user in enumerate(user_list):#estamos haciendo una validacion entre los dos id que tiene el user pasado como parametro y el user_saved(user saver recorre toda la user_list y en cada vuelta selecciona un usuario. por otro lado index es como un contador, pero no es un contador
        if saved_user.id == user.id:              #index funciona con la la funcion enumerate, la razon por la cual se declara a index antes que a saved_user es porque python primero pasa por la funcion enumerate para pasarle el numero de indic de a index, luego python coge el usuario y lo pasa a saved_user
            user_list[index] = user
            found = True
            #return {"Exito" : "Se actualizo el usuario"} si colocamos que retorne esto, pues abrá un error de validacion ya que como hemos mencionado response_model valida la salida de acuerdo al modelo base de User
            return user

    
    if found is False:
        raise HTTPException(status_code=404, detail="No existe ese usuario")
    






@app.delete("/user/{id}", status_code=204)
async def user(id : int):
    found = False
    for index, user_save in enumerate(user_list):
        if user_save.id == id:
            del user_list[index]
            found = True
            #return {"Exito" : "Usuario eliminado con exito"}
            """no tiene sentido colocar un return ya que colocamos que el status_code que devolvera por defecto, serà 204
            y la respuesta 204 no va a devolver nada asi nosotros quramos hacerlo
            Si queremos retornar algo pues devemos colocar un status_code que si lo haga como por ejemplo el 201"""
    if not found: 
        raise HTTPException(status_code=404, detail="Usuario no eliminado, Usuario no encontrado")
    
    



def search_user(id : int):
    usuario = filter(lambda user: user.id == id, user_list)
    try:
        return list(usuario)[0]
    except:
        #return {"error": "no existe el usuario proporcionado"} es mejor colocar que nos retorne None para que en las otras funcion podamos manejar los errores de una mejor manera
        return None        
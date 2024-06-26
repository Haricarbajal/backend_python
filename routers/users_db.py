#user db api

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db.models.user import User
from FastAPI.db.client import db_client

app = APIRouter(prefix="/usersdb",tags=["Usersdb"])



user_list = []





@app.get("/")
async def users():
    return user_list



@app.get("/{id}", response_model=User, status_code=200)
async def user(id : int):
    buscar_user = search_user(id)
    if buscar_user is None:
        raise HTTPException(status_code=404, detail="No existe el id de ese usuario")
    
    return buscar_user








@app.get("/")
async def userquery(id : int):
    buscar_user = search_user(id)
    if buscar_user is None:
        raise HTTPException(status_code=404, detail="El id proporcionado no existe en nigun usuario")
    
    return buscar_user







@app.post("/", response_model=User, status_code=201)
async def user(user : User):
    # if  type(search_user(user.id)) == User:
    #     raise HTTPException(status_code=404, detail="el usuario ya existe")

    user_dict = dict(user)
    del user_dict["id"]

    id = db_client.local.users.insert_one(user_dict).inserted_id

    db_client.local.users.find_one({"_id" : id})

    return user







@app.put("/", response_model=User, status_code=201)
async def user(user : User):
    found = False
    for index, saved_user in enumerate(user_list):
        if saved_user.id == user.id:              
            user_list[index] = user
            found = True
            return user

    
    if found is False:
        raise HTTPException(status_code=404, detail="No existe ese usuario")
    






@app.delete("/{id}", status_code=204)
async def user(id : int):
    found = False
    for index, user_save in enumerate(user_list):
        if user_save.id == id:
            del user_list[index]
            found = True
    if not found: 
        raise HTTPException(status_code=404, detail="Usuario no eliminado, Usuario no encontrado")
    
    



def search_user(id : int):
    usuario = filter(lambda user: user.id == id, user_list)
    try:
        return list(usuario)[0]
    except:
        return None        
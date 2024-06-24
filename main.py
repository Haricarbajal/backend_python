# main.py
from fastapi import FastAPI
from routers import products, users
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()


app.include_router(products.router)
app.include_router(users.app)
app.mount("/static", StaticFiles(directory="static"), name="youandme")

"""QUÉ ES LO QUE HACE name=youandme"""

"""primero colocaremos la instacia que hemos realizado de fastapi seguido de .mount, que no sirve para poder montar
un ------- static, luego colocares la manera en que lo llamaremos por http que en este caso es  "http:/localhost/8000/static"
para luego colocar con StaticFiles(directory="nombreDelaCaprpetaDondeTenemoEl.------Static") para luego poder llamarlo mediante
http de esta forma http:/localhost/8000/static/images/python.jpg"""

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/url")
def url():
    return {"url" : "www.mouredev.com"}


@app.get("/list-static-files")
async def list_static_files():
    # Obtener el montaje estático por nombre
    for route in app.routes:
        if hasattr(route, "name") and route.name == "youandme":
            static_dir = route.app.directory
            # Listar los archivos en el directorio estático
            files = []
            for root, _, filenames in os.walk(static_dir):
                for filename in filenames:
                    files.append(os.path.relpath(os.path.join(root, filename), static_dir))
            return {"files": files}
    return {"error": "Static mount not found"}
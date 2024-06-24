from fastapi import APIRouter

router = APIRouter(prefix="/products", tags=["Products"], responses={404 : {"mensaje" : "No encontrado"}})

products_list = ["producto1", "producto2", "producto3"]


@router.get("/")
async def products():
    return products_list

@router.get("/{id}")
async def product(id : int):
    return products_list[id]
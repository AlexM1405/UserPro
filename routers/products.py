from fastapi import APIRouter

router = APIRouter(prefix="/products",
                   responses={404: {"message": "Dont found it"}})

products_list = ["Producto 1", "Producto 2" , "Producto 3", "Producto 4"]

@router.get("/products")
async def products():
    return products_list

@router.get("/{id}")
async def products(id: int):
    return products_list[id]


from fastapi import APIRouter, HTTPException, Query, Depends
from src.schemas import ProductOut, ProductCreate, ProductUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_session
from src.models import Product
from src.repositories import products_repository

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

async def get_product_or_404(session:AsyncSession, product_id: int) -> Product:
    product = await products_repository.get_product(session, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="товар не найден")
    return product

@router.post("", response_model=ProductOut)
async def create_product(product_data: ProductCreate, session:AsyncSession = Depends(get_session)):
    return await products_repository.create_product(session, product_data)

@router.get("", response_model=list[ProductOut])
async def get_products_list(
    q: str | None  = Query(default=None, description='Поиск по подстроке'),
    in_stock: bool | None  = Query(default=None, description='Фильтр по наличию'),
    min_price: float | None  = Query(default=None, ge=0, description='Минимальная цена'),
    max_price: float | None  = Query(default=None, ge=0, description='Максимальная цена'),
    session: AsyncSession = Depends(get_session)
    ):

    return await products_repository.get_products_list(session, q, in_stock, min_price, max_price)

@router.get("/{product_id}", response_model=ProductOut)
async def get_product(product_id: int, session: AsyncSession = Depends(get_session)):
    return await get_product_or_404(session, product_id)

@router.put("/{product_id}", response_model=ProductOut)
async def put_product(product_id: int, 
                      product_data: ProductCreate, 
                      session: AsyncSession = Depends(get_session)):
    product = await get_product_or_404(session, product_id)
    return await products_repository.put_product(session, product, product_data)

@router.patch("/{product_id}", response_model=ProductOut)
async def patch_product(product_id: int, 
                        product_data: ProductUpdate, 
                        session: AsyncSession = Depends(get_session)):
    product = await get_product_or_404(session, product_id)
    return await products_repository.patch_product(session, product, product_data)

@router.delete("/{product_id}")
async def delete_product(product_id: int, session: AsyncSession = Depends(get_session)):
    product = await get_product_or_404(session, product_id)
    await products_repository.delete_product(session, product)
    return {"message": "Товар удалён"}
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.furniture.models import Furniture, ProductImage, Image
from database import get_db

router = APIRouter()

@router.get("/furniture")
async def read_furniture(db: AsyncSession = Depends(get_db)):
    try:
        query = (
            select(Furniture)
            .outerjoin(ProductImage, Furniture.id == ProductImage.furniture_id)
            .outerjoin(Image, ProductImage.image_id == Image.id)
        )
        result = await db.execute(query)
        furniture_list = result.scalars().all()

        furniture_data = []
        for item in furniture_list:
            furniture_data.append({
                "id": item.id,
                "name": item.name,
                "price": item.price,
                "characteristic": item.characteristic,
                "category": item.category,
                "images": [{"id": img.image.id, "image_url": img.image.image_url} for img in item.images if img.image]
            })

        return furniture_data
    except Exception as e:
        return {"error": str(e)}
    
__all__ = ["router"]

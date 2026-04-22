from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/items", tags=["items"])

# In-memory store (replace with DB later)
items_db = {
    1: {"id": 1, "name": "Apple", "price": 1.50},
    2: {"id": 2, "name": "Banana", "price": 0.75},
}


class Item(BaseModel):
    name: str
    price: float


@router.get("/")
def list_items():
    return list(items_db.values())


@router.get("/{item_id}")
def get_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]


@router.post("/")
def create_item(item: Item):
    new_id = max(items_db.keys()) + 1
    items_db[new_id] = {"id": new_id, **item.dict()}
    return items_db[new_id]

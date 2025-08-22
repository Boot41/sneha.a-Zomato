# app/routes/menu.py
from fastapi import APIRouter, HTTPException
from app.models import menu_item
from app.schemas.menu_item import MenuItemCreate, MenuItemResponse
from typing import List

router = APIRouter(
    tags=["Menu"]
)

# ✅ Add a menu item
@router.post("/{restaurant_id}", response_model=MenuItemResponse)
def create_menu_item(restaurant_id: int, item: MenuItemCreate):
    new_item = menu_item.add_menu_item(
        restaurant_id=restaurant_id,
        name=item.name,
        price=item.price,
        category=item.category,
        image=item.image
    )
    if not new_item:
        raise HTTPException(status_code=400, detail="Menu item could not be created")
    return MenuItemResponse(
        id=new_item["id"],
        name=new_item["name"],
        price=new_item["price"],
        category=new_item["category"],
        image=new_item["image"],
        created_at=new_item["created_at"]
    )


# Get all menu items for a restaurant
@router.get("/{restaurant_id}", response_model=List[MenuItemResponse])
def fetch_menu_items(restaurant_id: int):
    items = menu_item.get_menu_items_by_restaurant(restaurant_id)
    return [
        MenuItemResponse(
            id=i["id"],
            name=i["name"],
            price=i["price"],
            category=i["category"],
            image=i["image"],
            created_at=None  # since we didn't fetch created_at in query
        )
        for i in items
    ]


# Delete a menu item
@router.delete("/{menu_item_id}")
def remove_menu_item(menu_item_id: int):
    deleted = menu_item.delete_menu_item(menu_item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return {"message": "Menu item deleted successfully", "id": deleted[0] if deleted else None}

# # app/routes/resturants.py
# from fastapi import APIRouter, HTTPException
# from app.schemas.restaurant import RestaurantCreate, RestaurantResponse
# from app.models import resturants

# router = APIRouter(prefix="/restaurants", tags=["Restaurants"])


# # @router.post("/", response_model=RestaurantResponse)
# # def create_restaurant(rest: RestaurantCreate):
# #     new_rest = resturants.add_restaurant(
# #         rest.name, rest.description, rest.address, rest.phone
# #     )
# #     return new_rest





# # @router.post("/", response_model=RestaurantResponse)
# # def create_restaurant(restaurant: RestaurantCreate):
# #     new_restaurant = resturants.add_restaurant(
# #         restaurant.name, restaurant.description, restaurant.address, restaurant.phone
# #     )

# #     return {
# #         "id": new_restaurant[0],
# #         "name": new_restaurant[1],
# #         "description": new_restaurant[2],
# #         "address": new_restaurant[3],
# #         "phone": new_restaurant[4],
# #         "created_at": new_restaurant[5],
# #     }



# @router.post("/", response_model=RestaurantResponse)
# def create_restaurant(restaurant: RestaurantCreate):
#     new_restaurant = resturants.add_restaurant(
#         restaurant.name, restaurant.description, restaurant.address, restaurant.phone
#     )

#     return RestaurantResponse(
#         id=new_restaurant[0],
#         name=new_restaurant[1],
#         description=new_restaurant[2],
#         address=new_restaurant[3],
#         phone=new_restaurant[4],
#         created_at=new_restaurant[5],
#     )


# # @router.get("/", response_model=list[RestaurantResponse])
# # def list_restaurants():
# #     return resturants.get_restaurants()

# # @router.get("/", response_model=list[RestaurantResponse])
# # def list_restaurants():
# #     rows = resturants.get_restaurants()
# #     return [
# #         {
# #             "id": r[0],
# #             "name": r[1],
# #             "description": r[2],
# #             "address": r[3],
# #             "phone": r[4],
# #             "created_at": r[5],
# #         }
# #         for r in rows
# #     ]




# @router.get("/", response_model=list[RestaurantResponse])
# def list_restaurants():
#     rows = resturants.get_restaurants()
#     return [
#         RestaurantResponse(
#             id=r[0],
#             created_at=r[1],
#         )
#         for r in rows
#     ]



# @router.get("/{rest_id}", response_model=RestaurantResponse)
# def get_restaurant(rest_id: int):
#     rest = resturants.get_restaurant_by_id(rest_id)
#     if not rest:
#         raise HTTPException(status_code=404, detail="Restaurant not found")
#     return rest


# @router.delete("/{rest_id}")
# def remove_restaurant(rest_id: int):
#     deleted = resturants.delete_restaurant(rest_id)
#     if not deleted:
#         raise HTTPException(status_code=404, detail="Restaurant not found")
#     return {"message": "Restaurant deleted successfully"}







# app/routes/resturants.py
from fastapi import APIRouter, HTTPException, Depends
from app.schemas.restaurant import RestaurantCreate, RestaurantResponse
from app.models import resturants
from app.database import get_db

router = APIRouter(tags=["Restaurants"])


@router.post("/", response_model=RestaurantResponse)
def create_restaurant(restaurant: RestaurantCreate):
    # Get user ID from request (you'll need to implement auth middleware)
    # For now, we'll create the restaurant without owner association
    new_restaurant = resturants.add_restaurant(
        restaurant.name, restaurant.description, restaurant.address, restaurant.phone
    )
    if not new_restaurant:
        raise HTTPException(status_code=400, detail="Restaurant could not be created")
    
    return RestaurantResponse(
        id=new_restaurant["id"],
        name=new_restaurant["name"],
        description=new_restaurant["description"],
        address=new_restaurant["address"],
        phone=new_restaurant["phone"],
        created_at=new_restaurant["created_at"]
    )




@router.get("/", response_model=list[RestaurantResponse])
def list_restaurants():
    rows = resturants.get_restaurants()
    return [RestaurantResponse(id=r["id"], name=r["name"]) for r in rows]


@router.get("/{rest_id}", response_model=RestaurantResponse)
def get_restaurant(rest_id: int):
    rest = resturants.get_restaurant_by_id(rest_id)
    if not rest:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return rest


@router.delete("/{rest_id}")
def remove_restaurant(rest_id: int):
    deleted = resturants.delete_restaurant(rest_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return {"message": "Restaurant deleted successfully"}

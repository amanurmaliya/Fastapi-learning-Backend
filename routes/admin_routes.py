from fastapi import APIRouter, HTTPException, Depends
from configs.database import user_collection, order_collection, product_collection

from bson import ObjectId

from utils.auth_dependencies import admin_required

router = APIRouter()


# view All Users
@router.get("/admin/users")
def get_all_users(current_user: dict = Depends(admin_required)):
    users = list(user_collection.find())
    
    for user in users:
        user["id"] = str(user["_id"])
        del user["_id"]
        del user["password"]
        
    return users

# Delete a User
@router.delete("/admin/users/{user_id}")
def delete_user(user_id : str, current_user: dict = Depends(admin_required)):
    result = user_collection.delete_one({"_id": ObjectId(user_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User Not Found")
    
    return {"message" : "User Deleted Successfully"}


# Delete a order
@router.delete("/admin/orders/{order_id}")
def delete_order(order_id : str , current_user: dict = Depends(admin_required)):
    
    result = order_collection.delete_one({"_id" : ObjectId(order_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Order Not Found")
    
    return {"message" : "Order deleted Successfully"}

# View all products
@router.get("/admin/products")
def get_all_products(current_user: dict = Depends(admin_required)):
    products = list(product_collection.find())
    
    for product in products:
        product["id"] = str(product["_id"])
        
        del product["_id"]
        
        
    return products



from fastapi import APIRouter, HTTPException, Depends

from models.cart_models import CartItem, UpdateCartItem
from configs.database import cart_collection , product_collection

from utils.auth_dependencies import get_current_user

from bson import ObjectId


router = APIRouter()


# Add item to cart
@router.post("/cart/{user_id}/add")
def add_to_cart(user_id: str, item : CartItem , current_user: dict = Depends(get_current_user)):
    if str(current_user["_id"]) != (user_id) and current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    # Validate product exxistence
    product = product_collection.find_one({"_id": item.product_id})
    
    if not product:
        raise HTTPException(status_code=404,
                            detail = "Sorry No Product Found")
        
    existing_cart = cart_collection.find_one({"user_id": user_id})
    
    if not existing_cart:
        cart_collection.insert_one({
            "user_id" : user_id,
            "items" : [{"product_id" : item.product_id, "quantity" : item.quantity}]
        })
        
    else:
        # Check if the product already exists
        items = existing_cart["items"]
        
        for i in items:
            if i["product_id"] == item.product_id:
                i["quantity"] += item.quantity
                break
        else:
            items.append({"product_id": item.product_id, "quantity": item.quantity})
            
        cart_collection.update_one({"user_id" : user_id}, {"$set" : {"items": items}})
        
    return {"message": "Product added to Cart"}

# view Cart
@router.get("/cart/{user_id}")
def get_cart(user_id: str, current_user: dict = Depends(get_current_user)):
    
    if str(current_user["_id"]) != user_id and current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    
    cart = cart_collection.find_one({"user_id": user_id})
    
    if not cart:
        return {"items": [], "total_price" : 0}
    
    total = 0
    enriched_items = []
    
    for item in cart["items"]:
        product = product_collection.find_one({"_id": ObjectId(item["product_id"])})
        
        if product :
            price = product["price"]
            subtotal = price * item["quantity"]
            total += subtotal
            enriched_items.append({
                "product_id" : item["product_id"],
                "name" : product["name"],
                "price": price,
                "quantity" : item["quantity"],
                "subtotal" : subtotal
            })
            
    return {"items": enriched_items, "total_price" : price}
    
    
# Update Quantity 
@router.put("/cart/{user_id}/update")
def update_cart_items(user_id: str, item: UpdateCartItem, current_user: dict = Depends(get_current_user)):
    
    if str(current_user["_id"]) != user_id and current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    
    cart = cart_collection.find_one({"user_id" : user_id}) # here if you will use find_one it will return the cursor of objects
    
    if not cart:
        raise HTTPException(status_code=404, detail="User Has no item in the cart")
    
    updated = False
    
    for i in cart["items"]:
        if i["product_id"] == item.product_id:
            i["quantity"] = item.quantity
            updated =  True
            break
        
    if not updated:
        raise HTTPException(status_code = 404, detail = "Item not found in cart")
    
    cart_collection.update_one({"user_id" : user_id}, {"$set" : {"items" : cart["items"]}})
    
    
    return {"message": "Quantity Updated"}

# Remove Products
@router.delete("/cart/{user_id}/remove/{product_id}")
def remove_cart_item(user_id : str, product_id : str, current_user: dict = Depends(get_current_user)):
    
    if str(current_user["_id"]) != user_id and current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    
    cart = cart_collection.find_one({"user_id" : user_id})
    
    if not cart: 
        raise HTTPException(status_code = 404, detail="Cart not Found")
    
    items = [i for i in cart["items"] if i["product_id"] != product_id]
    
    cart_collection.update_one({"user_id" : user_id}, {"$set" : {"items" : items}})
    
    return {"message" : "Item Removed From Cart"}


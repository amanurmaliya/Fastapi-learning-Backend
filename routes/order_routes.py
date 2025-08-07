from fastapi import APIRouter, HTTPException
from configs.database import order_collection, product_collection
from models.order_models import Order
from bson import ObjectId


router = APIRouter()


# Place Order 
@router.post("/orders")
def place_order(order: Order):
    # 1. Decrease stock for each product
    for product_id in order.products:
        # Convert string to ObjectId
        obj_id = ObjectId(product_id)

        # Check if product exists
        product = product_collection.find_one({"_id": obj_id})
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found")

        # Check stock
        if product.get("stock", 0) <= 0:
            raise HTTPException(status_code=400, detail=f"Product '{product.get('name')}' is out of stock")

        # Decrease stock by 1
        product_collection.update_one(
            {"_id": obj_id},
            {"$inc": {"stock": -1}}
        )

    # 2. Insert the order
    res = order_collection.insert_one(order.dict())

    return {
        "success": res.acknowledged,
        "message": "Order Created Successfully",
        "order_id": str(res.inserted_id)
    }

# Get all orders
@router.get("/orders")
def get_orders():
    orders_cursor = order_collection.find()
    
    orders = []
    for order in orders_cursor:
        order["id"] = str(order["_id"])
        del order["_id"]
        orders.append(order)
        
    return orders

 
from fastapi import APIRouter, HTTPException, Query, Depends
from bson import ObjectId
from models.product_models import Product, ProductSearch, ProductUpdate, ProductFilter
from configs.database import product_collection
from typing import Optional
from utils.auth_dependencies import get_current_user, admin_required

router = APIRouter()


# GEt all the products with pagination
@router.get("/product-list")
def get_all_products(page: int = 1, limit: int = 10):
    skip = (page - 1) * limit
    products = list(product_collection.find().skip(skip).limit(limit))
    
    for p in products:
        p["id"] = str(p["_id"])
        del p["_id"]
    
    return products

# Get the product detail
@router.get("/product/{id}")
def get_product(id: str):
    product = product_collection.find_one({"_id" : ObjectId(id)})
    
    if not product:
        raise HTTPException(status_code = 404, detail = "Product not found")
    
    product["id"] = str(product["_id"])
    
    del product["_id"]
    
    return product  

# Set the New products
@router.post("/add-product")
def add_product(product : Product, current_user: dict = Depends(admin_required)):
    
    # The mongodb accepts the dictionary data type of python hence we have converted it
    res = product_collection.insert_one(product.model_dump())
   
    return {"success":res.acknowledged, "message":"Product Added Successfully", "id":str(res.inserted_id)}

# Update The Product
@router.post("/product/{id}")
def update_product(id: str, update: ProductUpdate, current_user: dict = Depends(admin_required)):
    result = product_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set" : {k: v for k, v in update.model_dump().items() if v is not None}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"message" : "Product updated successfully"}


# Delete the product
@router.delete("/product/{id}")
def delete_product(id: str, current_user: dict = Depends(admin_required)):
    result = product_collection.delete_one({"_id" : ObjectId(id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code = 404, detail = "Product Not Found")
    
    return {"message" : "Product Deleted Successfully"}


# Search Product
@router.post("/search-product")
def search_product(data : ProductSearch):
    query = {"name" : {"$regex": data.query, "$options" : "i"}} 
    
    """ 🎛️ What is $options: "i"?
This is a modifier for the regex.

"i" stands for insensitive — i.e., case-insensitive match.

Other options include:

"m" → multi-line

"x" → ignore whitespace in regex

"s" → dot matches all (including newline)

But here, you're just using "i" to make sure searches match regardless of case. """
    
    products = list(product_collection.find(query))
    
    for product in products:
        product["id"] = str(product["_id"])
        del product["_id"]
        
    return products


# Filter Product
@router.post("/filter-products")
def filter_products(filters: ProductFilter):
    
    query = {}
    
    if filters.category:
        query["category"] = filters.category
        
    if filters.min_price is not None and filters.max_price is not None:
        query["price"] = {}
        
        if filters.min_price is not None:
            query["price"]["$gte"] = filters.min_price
        if filters.max_price is not None:
            query["price"]["$lte"] = filters.max_price
            
    if filters.min_rating is not None:
        query["rating"] = {"$gte" : filters.min_rating}
        
    products = list(product_collection.find(query))
    
    for product in products:
        product["id"] = str(product["_id"])
        del product["_id"]
        
    
    return products
   
    

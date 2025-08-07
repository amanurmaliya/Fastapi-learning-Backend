from fastapi import APIRouter, HTTPException
from bson import ObjectId
from models.product_models import Product, ProductSearch
from configs.database import product_collection


router = APIRouter()


# Get all the products list
@router.get("/product-list")
def get_all_products():
    products = list(product_collection.find())
    
    for p in products:
        p["id"] = str(p["_id"]) # make a new feild id and then delete the _id part
        del p["_id"]
        
    return products


# Get the products
@router.post("/add-product")
def add_product(product : Product):
    
    # The mongodb accepts the dictionary data type of python hence we have converted it
    res = product_collection.insert_one(product.dict())
   
    return {"success":res.acknowledged, "message":"Product Added Successfully", "id":str(res.inserted_id)}

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
    
    

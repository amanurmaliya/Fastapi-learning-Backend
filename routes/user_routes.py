from fastapi import APIRouter, HTTPException, Request, Depends
from models.user_models import User, UserLogin, UserOut

from configs.database import user_collection

from bson import ObjectId
from utils.auth_utils import hash_password, verify_password, generate_token
from utils.auth_dependencies import admin_required



router = APIRouter()

@router.post("/auth/register")
def register_user(user: User):
    if user_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already Exists")
    
    user_dict = user.model_dump()
    user_dict["password"] = hash_password(user.password)
    user_dict["role"] = "user"
    
    result = user_collection.insert_one(user_dict)
    user_out = {
        "id" : str(result.inserted_id),
        "name" : user.name,
        "email" : user.email,
        "role" : "user"
    }
    
    return user_out


@router.post("/auth/login")
def login_user(user: UserLogin):
    db_user = user_collection.find_one({"email": user.email})
    
    
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code = 404, detail="Invalid Credentials")
    
    token = generate_token({"user_id" : str(db_user["_id"]), "email" : db_user["email"]})
    
    return {"access_token" : token}



# === NEW: register-admin (bootstrap-safe) ===
@router.post("/auth/register-admin", response_model=UserOut)
def register_admin(user: User, request: Request):
    """
    Create an admin user.
    - If there is NO admin in DB yet (fresh DB), this endpoint allows creating the first admin WITHOUT auth.
    - If an admin already exists, this endpoint requires Authorization header with an admin JWT.
    """
    # Count existing admins
    admin_count = user_collection.count_documents({"role": "admin"})

    if admin_count > 0:
        # Admin(s) already exist -> require Authorization header and verify admin role
        auth = request.headers.get("Authorization")
        if not auth:
            raise HTTPException(status_code=401, detail="Admin credentials required")
        try:
            token = auth.split(" ")[1]
            payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            if payload.get("role") != "admin":
                raise HTTPException(status_code=403, detail="Admin access required")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid token")

    # create admin
    if user_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already exists")
    user_dict = user.dict()
    user_dict["password"] = hash_password(user.password)
    user_dict["role"] = "admin"
    result = user_collection.insert_one(user_dict)
    return {"id": str(result.inserted_id), "name": user.name, "email": user.email, "role": "admin"}


# === NEW: promote an existing user to admin (admin only) ===
@router.put("/auth/promote/{user_id}")
def promote_user(user_id: str, current_user: dict = Depends(admin_required)):
    """
    Promote an existing user to role='admin'. Only callable by admins.
    """
    res = user_collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"role": "admin"}})
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    user = user_collection.find_one({"_id": ObjectId(user_id)})
    return {"id": str(user["_id"]), "email": user["email"], "role": user["role"]}
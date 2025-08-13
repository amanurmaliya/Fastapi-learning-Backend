from fastapi import Depends, HTTPException, status

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

import jwt
import os 
from dotenv import load_dotenv
from configs.database import user_collection

from bson import ObjectId


load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET", "secret123")

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        
        user_id = payload.get("user_id")
        
        if not user_id:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "User Not Found")
        
        user = user_collection.find_one({"_id" : ObjectId(user_id)})
        
        if not user:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "No User Found")
        
        return user
    
    except jwt.ExpiredSignatureError:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Token Expired")
        
    except jwt.InvalidTokenError:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid Token")
    

def admin_required(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return current_user

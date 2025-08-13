from pydantic import BaseModel, EmailStr

from typing import Optional

class User(BaseModel):
    name : str
    email : EmailStr
    password : str
    

class UserLogin(BaseModel):
    email : EmailStr
    password : str
    
class UserOut(BaseModel):
    id: str
    name : str
    email : EmailStr
    role : Optional[str] = "user"
    

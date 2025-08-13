import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv();

from fastapi import FastAPI
from routes import order_routes, product_routes, user_routes, cart_routes, admin_routes

from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

# ACcess the vaiables
FRONTEND_API = os.getenv("FRONTEND_API")

# ✅ Add the CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins= [FRONTEND_API, "https://fastapi-learning-frontend.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],              # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],              # Allow all headers
)

app.include_router(product_routes.router, prefix="/api/v1")

app.include_router(order_routes.router, prefix="/api/v1")

app.include_router(user_routes.router, prefix="/api/v1")

app.include_router(cart_routes.router, prefix="/api/v1")

app.include_router(admin_routes.router, prefix="/api/v1")
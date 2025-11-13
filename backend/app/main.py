from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .routes import user_routes, item_routes, cart_routes, order_routes, admin_routes
from .database import engine
from .models import user_model
from.dependencies import get_current_user

# Create database tables
user_model.Base.metadata.create_all(bind=engine)

# Intializing the FastAPI app
app = FastAPI(
    title="Fidgi API",
    description="Fidget toy e-commerce platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Configure for production, allow_origins=["https://swagspinners.com", "https://www.swagspinners.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registering route modules
app.include_router(user_routes.router)
#app.include_router(item_routes.router)
#app.include_router(cart_routes.router)
#app.include_router(order_routes.router)
#app.include_router(admin_routes.router)


@app.get("/health")
def health_check():
    return {"status": "healthy"}

    #try:
    #    db.execute("SELECT 1")
    #    return {"status": "healthy"}
    #except Exception as e:
    #   return {"status": "unhealthy", "error": str(e)}


# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "SwagSpinners API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }
    
@app.get("/me")
def read_users_me(current_user = Depends(get_current_user)):
    return {
        "id": current_user.clerk_user_id,
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
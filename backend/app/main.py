from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import webhooks, user_routes, item_routes, cart_routes

# Intializing the FastAPI app
app = FastAPI(
    title="Fidgi API",
    description="Fidget toy e-commerce platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production, allow_origins=["https://swagspinners.com", "https://www.swagspinners.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registering route modules
app.include_router(webhooks.router)
app.include_router(user_routes.router)
app.include_router(item_routes.router)
app.include_router(cart_routes.router)
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
    
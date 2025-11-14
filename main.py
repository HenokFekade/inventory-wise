from fastapi import FastAPI

# initialize server
app = FastAPI(lifespan=lifespan, title="Inventory Wise API")

@app.get("/health")
def health():
    return {
        "status": 200,
        "message": "Inventory Wise API Server is running successfully",
    }

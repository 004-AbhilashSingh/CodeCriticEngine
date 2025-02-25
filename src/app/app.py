from fastapi import FastAPI
import uvicorn

from src.controllers.HealthController import router as HealthRouter

app = FastAPI()

app.include_router(HealthRouter)

if __name__ == "__main__":
    uvicorn.run(app,host="127.0.0.1",port=8080)
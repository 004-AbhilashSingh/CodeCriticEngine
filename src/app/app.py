from fastapi import FastAPI
import uvicorn

from src.controllers.HealthController import router as HealthRouter
from src.controllers.LlmController import router as LLMRouter

app = FastAPI()

app.include_router(HealthRouter)
app.include_router(LLMRouter)

if __name__ == "__main__":
    uvicorn.run(app,host="127.0.0.1",port=8080)
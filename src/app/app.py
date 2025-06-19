from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from src.controllers.HealthController import router as HealthRouter
from src.controllers.LlmController import router as LLMRouter

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(HealthRouter)
app.include_router(LLMRouter)


if __name__ == "__main__":
    uvicorn.run(app,host="127.0.0.1",port=8100)
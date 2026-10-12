
from fastapi import FastAPI
from api.routes import router

app = FastAPI(
    title="Enterprise RAG Agent",
    description="Enterprise Knowledge Base RAG API",
    version="1.0.0",
)

app.include_router(router)


@app.get("/")
def root():
    return {"message": "Enterprise RAG Agent API is running"}


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Enterprise RAG Agent",
    }

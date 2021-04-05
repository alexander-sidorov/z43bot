import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "asgi:app",
        host="localhost",
        log_level="debug",
        port=8000,
        reload=True,
    )

import uvicorn

if __name__ == "__main__":
    uvicorn.run("backend.api.api:app")
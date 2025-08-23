from fastapi import FastAPI

app = FastAPI()

@app.get("/health_cehch")
async def health_check():
    return {"status": "Db service started"}
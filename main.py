import io

from fastapi import FastAPI, UploadFile,File
from fastapi.responses import JSONResponse
import pypdf

from routes import resume

app=FastAPI()

@app.get("/health")
def health_check():
    return {"status": "healthy"}

app.include_router(resume.router)
from fastapi import FastAPI, UploadFile, File
from pymongo import MongoClient
from bson import ObjectId
import uvicorn
import os
import io
import gridfs

app = FastAPI()

# Initialize MongoDB client
client = MongoClient('mongodb://mongo:DgycJxuOGTtPTGkZNwFBMPjWUJrnxGZI@viaduct.proxy.rlwy.net:21552')
db =  client['test']
fs = gridfs.GridFS(db)

@app.post("/uploadimage/")
async def upload_image(file: UploadFile = File(...)):
    contents = await file.read()
    image_id = fs.put(io.BytesIO(contents), filename=file.filename)
    return {"image_id": str(image_id)}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=os.getenv("PORT", default=8080), log_level="info")
from fastapi import FastAPI, UploadFile, File
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import uvicorn
import os
import io
import gridfs

app = FastAPI()

# Initialize MongoDB client
client = AsyncIOMotorClient('mongodb://mongo:DgycJxuOGTtPTGkZNwFBMPjWUJrnxGZI@viaduct.proxy.rlwy.net:21552')
db = client['image_database']
fs = gridfs.GridFS(db)

@app.post("/uploadimage/")
async def upload_image(file: UploadFile = File(...)):
    contents = await file.read()
    image_id = fs.put(io.BytesIO(contents), filename=file.filename)
    return {"image_id": str(image_id)}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=os.getenv("PORT", default=5000), log_level="info")
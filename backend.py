from fastapi import FastAPI, UploadFile, File
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import io
import gridfs

app = FastAPI()

# Initialize MongoDB client
client = AsyncIOMotorClient('mongodb://localhost:27017')
db = client['image_database']
fs = gridfs.GridFS(db)

@app.post("/uploadimage/")
async def upload_image(file: UploadFile = File(...)):
    contents = await file.read()
    image_id = fs.put(io.BytesIO(contents), filename=file.filename)
    return {"image_id": str(image_id)}
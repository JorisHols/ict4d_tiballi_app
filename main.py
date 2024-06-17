from fastapi import FastAPI, UploadFile, File
from pymongo import MongoClient
from bson import ObjectId
from PIL import Image, ExifTags
import uvicorn
import os
import io
import gridfs
from PIL.TiffImagePlugin import IFDRational


app = FastAPI()

# Initialize MongoDB client
client = MongoClient('mongodb://mongo:DgycJxuOGTtPTGkZNwFBMPjWUJrnxGZI@viaduct.proxy.rlwy.net:21552')
db =  client['test']
fs = gridfs.GridFS(db)

def handle_exif_data(raw_metadata):
    metadata = {}
    for k, v in raw_metadata.items():
        if k in ExifTags.TAGS and isinstance(ExifTags.TAGS[k], str):
            if isinstance(v, IFDRational):
                metadata[ExifTags.TAGS[k]] = float(v)
            else:
                metadata[ExifTags.TAGS[k]] = v
    return metadata

@app.post("/uploadimage/")
async def upload_image(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    image_id = fs.put(io.BytesIO(contents), filename=file.filename)

    raw_metadata = image._getexif()
    metadata = handle_exif_data(raw_metadata)

    print(metadata)
    return {"image_id": str(image_id), "metadata": metadata}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=os.getenv("PORT", default=8080), log_level="info")
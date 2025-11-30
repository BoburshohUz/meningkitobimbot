from fastapi import APIRouter,File,UploadFile,HTTPException
from PIL import Image
from pyzbar.pyzbar import decode
import io

router=APIRouter()

@router.post("/scan_qr")
async def scan_qr(file:UploadFile=File(...)):
    raw=await file.read()
    try:
        img=Image.open(io.BytesIO(raw))
    except:
        raise HTTPException(400,"Rasm noto‘g‘ri")
    qr=decode(img)
    if not qr:
        return {"ok":False,"message":"QR topilmadi"}
    return {"ok":True,"results":[{"data":d.data.decode(),"type":d.type} for d in qr]}

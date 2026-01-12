from fastapi import FastAPI, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import shutil
import os

# importa o motor OMR existente
from main import process_omr

app = FastAPI(title="OMR API")

# libera acesso externo (Base44, apps, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/scan")
async def scan_omr(
    file: UploadFile = File(...),
    total_questoes: int = Query(25)
):
    # salva imagem temporariamente
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        shutil.copyfileobj(file.file, tmp)
        image_path = tmp.name

    try:
        # chama o OMR original
        resultado = process_omr(
            image_path=image_path,
            total_questions=total_questoes
        )
        return resultado
    finally:
        os.remove(image_path)

# Importar módulos y funciones compartidos
from services import *
from models import *
from fastapi import APIRouter, Request, Response, File, UploadFile
from fastapi import logger as log
from fastapi.responses import FileResponse, JSONResponse

# Crear instancias de clases compartidas
audio_service = AudioService()
coqui_service = CoquiService()
speechbrain_service = SpeechBrainService()
polly_service = PollyService()


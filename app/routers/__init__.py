# Importar módulos y funciones compartidos
from services.audio_service import AudioService
from services.coqui_service import CoquiService
from services.speechbrain_service import SpeechBrainService
from models import *
from fastapi import APIRouter, Request, Response, File, UploadFile
from fastapi import logger as log
from fastapi.responses import FileResponse, JSONResponse

# Crear instancias de clases compartidas
audio_service = AudioService()
coqui_service = CoquiService()
speechbrain_service = SpeechBrainService()


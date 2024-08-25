import logging
from fastapi.responses import JSONResponse
from fastapi import Request
from . import *

import os.path

common_router = APIRouter()

# Configure the logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@common_router.get("/audios")
def get_audio_filenames():
    return JSONResponse(content=AudioService().get_audio_filenames())


@common_router.get("/audio")
def get_audio_by_filename(request: Request):
    params = request.query_params
    if 'filename' not in params:
        return JSONResponse(content=MessageResponse(message="No se ha especificado el nombre del archivo de audio.").model_dump())

    response: MessageResponse = AudioService().get_audio_by_filename(params['filename'])

    if os.path.isfile(response.message):
        return FileResponse(path=response.message, media_type="audio/wav")
    else:
        return JSONResponse(content=MessageResponse(message="Error al obtener el archivo de audio.").model_dump())

@common_router.post("/upload")
def upload_audio(request: Request):
    if (request.body is None):
        return JSONResponse(content=MessageResponse(message="No se ha enviado ningún archivo.").model_dump())
    
    audio_path = AudioService().save_file(request.body)
    return JSONResponse(content=MessageResponse(message=audio_path).model_dump())
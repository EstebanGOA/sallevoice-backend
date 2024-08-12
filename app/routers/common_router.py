from fastapi.responses import JSONResponse
from . import *

import os.path

common_router = APIRouter()


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

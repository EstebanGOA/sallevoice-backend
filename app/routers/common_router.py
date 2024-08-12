from . import *

import os.path

common_router = APIRouter()

@common_router.get("/audios")
def get_audio_filenames():
    return AudioService().get_audio_filenames()

@common_router.get("/audio")
def get_audio_by_filename(request: Request):
    params = request.query_params
    if 'filename' not in params: 
        return Response(content="No se ha especificado el nombre del archivo de audio.", media_type="text/plain")
    
    log.logger.info(f"Se ha solicitado el archivo de audio {params['filename']}")
           
    filepath = AudioService().get_audio_by_filename(params['filename'])
    
    if os.path.isfile(filepath): 
        log.logger.info(f"Se ha encontrado el archivo de audio en la ruta {filepath}, devolviendo archivo.")
        return FileResponse(path=filepath, media_type="audio/wav")
    else: 
        log.logger.error(f"No se ha encontrado el archivo de audio en la ruta {filepath}")
        return Response(content="Error al obtener el archivo de audio.", media_type="text/plain")
    

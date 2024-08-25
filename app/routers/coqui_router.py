import logging
from fastapi.responses import JSONResponse
from . import *

import os.path
import json

cq_router = APIRouter()

# Configure the logger
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@cq_router.post("/generate", response_description="Genera un archivo de audio a partir de un texto.")
async def generate_audio(request: CoquiRequest):
    """Genera un archivo de audio a partir de un texto.

    Args:
        text (str): Texto a convertir en audio.
        model_name (str, optional): Nombre del modelo a utilizar. Defaults to "tts_models/spa/fairseq/vits".

    Returns:
        _type_: _description_
    """
    logger.info(request)
    response = coqui_service.generate_audio(request)
    if response.message is not None:
        return JSONResponse(content=response.model_dump())
    else:
        return JSONResponse(content=MessageResponse("Error al generar el archivo de audio.").model_dump())


@cq_router.post('/clone', response_description="Genera un archivo de audio a partir de un texto y un audio de referencia.")
async def generate_voice_cloning(request: CoquiRequest):
    """Genera un archivo de audio a partir de un texto y un audio de referencia.

    Args:
        text (str): Texto a convertir en audio.
        model_name (str): Nombre del modelo a utilizar.
        speaker_input (UploadFile): Archivo de audio de referencia. Se espera un archivo de audio en formato WAV.
        language (str, optional): Idioma del modelo. Únicamente necesario si el modelo es multilenguaje. Por defecto es español.

    Returns:
        _type_: El archivo de audio generado.
    """
    response = await coqui_service.generate_voice_cloning(request)
    if response.message is not None:
        return JSONResponse(content=response.model_dump())
    else:
        return JSONResponse(content=MessageResponse("Error al generar el archivo de audio.").model_dump())


@cq_router.get('/models', response_description="Lista los modelos disponibles.")
async def get_models():
    """Recoge la lista de modelos disponibles para Coqui TTS.
    """
    return JSONResponse(content=coqui_service.list_models().model_dump())


@cq_router.get('/model', response_description="Muestra información relevante del modelo seleccionado.")
async def get_model_info(request: Request):
    """Recoge la lista de speakers disponibles para un modelo.
    """
    params = request.query_params
    if 'model_name' not in params:
        return JSONResponse(content=MessageResponse("No se ha especificado el nombre del modelo."))

    return JSONResponse(content=coqui_service.get_model_info(params['model_name']).model_dump())


import json
import logging
from . import *

polly_router = APIRouter()

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@polly_router.post("/synthesize", response_description="Genera un archivo de audio a partir de un texto.")
async def synthesize_audio(request: PollyRequest): 
    response = polly_service.speech_synthesis(request)
    return JSONResponse(content=MessageResponse(message=response).model_dump())

@polly_router.post("/voices", response_description="Lista las voces disponibles.")
async def list_voices(request: PollyVoiceRequest): 
    response = polly_service.list_voices(request) 
    return JSONResponse(content=response.model_dump())
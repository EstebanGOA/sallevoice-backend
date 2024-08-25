from . import *

sb_router = APIRouter()

@sb_router.get("/models", response_description="Lista los modelos disponibles.")
async def get_models():
    """Obtiene la lista de modelos disponibles para SpeechBrain.
    """
    return JSONResponse(content=speechbrain_service.list_models().model_dump())
        
@sb_router.get("/vocoders", response_description="Lista los vocoders disponibles.")
async def get_vocoders(): 
    """Obtiene la lista de vocoders disponibles para SpeechBrain.
    """
    return JSONResponse(content=speechbrain_service.list_vocoders().model_dump())

@sb_router.post("/generate", response_description="Genera un archivo de audio a partir de un texto.")
async def generate_audio(request: SpeechBrainRequest):
    """Recibe la petición para generar un archivo de audio a partir de un texto. 

    Args:
        text (str): Texto a convertir a audio. 
        vocoder (str, optional): Nombre del vocoder a utilizar.
        tts (str, optional):: Nombre del modelo a utilizar.
    """
    response = speechbrain_service.generate_audio(request)
    return JSONResponse(content=response.model_dump())
    
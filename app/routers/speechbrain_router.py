from . import *

sb_router = APIRouter()

@sb_router.get("/models", response_description="Lista los modelos disponibles.")
async def get_models():
    """Obtiene la lista de modelos disponibles para SpeechBrain.
    """
    return speechbrain_service.list_models()
        
@sb_router.get("/generate", response_description="Genera un archivo de audio a partir de un texto.")
async def generate_audio(text: str, vocoder: str = "speechbrain/tts-hifigan-ljspeech", tts: str = "speechbrain/tts-tacotron2-ljspeech"):
    """Recibe la petición para generar un archivo de audio a partir de un texto. 

    Args:
        text (str): Texto a convertir a audio. 
        vocoder (str, optional): Nombre del vocoder a utilizar.
        tts (str, optional):: Nombre del modelo a utilizar.
    """
    audio_path = speechbrain_service.generate_audio(tts=tts, vocoder=vocoder, text=text)
    return FileResponse(path=audio_path, media_type="audio/wav")
    
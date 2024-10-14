import logging
from fastapi import FastAPI
from routers.coqui_router import cq_router
from routers.common_router import common_router
from routers.speechbrain_router import sb_router
from routers.polly_router import polly_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="SalleVoice API",
    description="API para la generación de voz a partir de texto.",
    version="0.1.0",
    debug=True 
)

# Direcciones IP permitidas para CORS
origins = [
    'http://localhost:4200'  # Aplicación Angular en desarrollo
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(common_router, prefix="/api", tags=["Common"])
app.include_router(cq_router, prefix="/api/coqui", tags=["Coqui TTS"])
app.include_router(sb_router, prefix="/api/speechbrain", tags=["SpeechBrain"])
app.include_router(polly_router, prefix="/api/polly", tags=["Polly"])

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

@app.get("/")
async def root():
    """Función de prueba para verificar que la API está funcionando correctamente. 

    Returns:
        _type_: Mensaje de bienvenida de la API. 
    """
    return {"message": "Bienvenido a la API de SalleVoice. Esto es un mensaje de prueba para verificar que la API está funcionando correctamente."}

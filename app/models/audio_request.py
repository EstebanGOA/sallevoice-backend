from pydantic import BaseModel

class ModelRequest(BaseModel):
    name: str

class CoquiRequest(BaseModel): 
    text: str
    model: str = "tts_models/spa/fairseq/vits"
    speaker_input: bytes = None
    language: str = "es" 

class BrainSpeechRequest(BaseModel):
    text: str
    vocoder: str = "speechbrain/tts-hifigan-ljspeech"
    tts: str = "speechbrain/tts-tacotron2-ljspeech"
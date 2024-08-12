from typing import List, Optional
from pydantic import BaseModel


class ModelRequest(BaseModel):
    name: str


class CoquiRequest(BaseModel):
    text: str
    model: str = "tts_models/spa/fairseq/vits"
    speaker: Optional[str] = None
    language: Optional[str] = "es"
    speaker_input: Optional[bytes] = None


class BrainSpeechRequest(BaseModel):
    text: str
    vocoder: str = "speechbrain/tts-hifigan-ljspeech"
    tts: str = "speechbrain/tts-tacotron2-ljspeech"


class MessageResponse(BaseModel):
    message: str


class ListResponse(BaseModel):
    list: List[str]


class ModelResponse(BaseModel):
    is_multi_speaker: bool
    speakers: List[str]
    is_multi_lingual: bool
    languages: List[str]

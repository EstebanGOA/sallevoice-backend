from typing import List
from pydantic import BaseModel
from fastapi import UploadFile

class ModelRequest(BaseModel):
    name: str


class CoquiRequest(BaseModel):
    text: str
    model: str
    speaker: str | None = None
    language: str | None = None
    speaker_input: str | None = None


class SpeechBrainRequest(BaseModel):
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

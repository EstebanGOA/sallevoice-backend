from typing import List, Optional
from pydantic import BaseModel
from fastapi import UploadFile

class ModelRequest(BaseModel):
    name: str

class CoquiCloneRequest(BaseModel):
    speaker_name: str
    speaker_input: str

class PollyRequest(BaseModel):
    Engine: str
    LanguageCode: str
    Text: str
    TextType: str = "text"
    VoiceId: str

class PollyVoice(BaseModel):
    Gender: str
    Id: str
    LanguageCode: str
    LanguageName: str
    Name: str

class PollyVoiceResponse(BaseModel):
    Voices: List[PollyVoice]

class PollyVoiceRequest(BaseModel):
    Engine: str = 'standard'
    LanguageCode: str = 'es-ES'
    IncludeAdditionalLanguageCodes: bool = True

class CoquiRequest(BaseModel):
    text: str
    model: str | None = None
    speaker: str | None = None
    language: str | None = None

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

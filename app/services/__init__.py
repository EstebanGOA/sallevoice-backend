import logging
from models import *
from fastapi import UploadFile, File
from .audio_service import AudioService
from .coqui_service import CoquiService
from .speechbrain_service import SpeechBrainService
from .polly_service import PollyService

BASE_OUTPUT_PATH = "resources/outputs/"
BASE_INPUT_PATH = "resources/inputs/"
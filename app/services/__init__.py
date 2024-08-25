from models import *
from services import *
from fastapi import UploadFile, File
from .audio_service import AudioService

BASE_OUTPUT_PATH = "resources/outputs/"
BASE_INPUT_PATH = "resources/inputs/"

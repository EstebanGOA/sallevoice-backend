import json
import os
from . import *

import uuid
import torch
import base64
import logging
import io

from fastapi import HTTPException
from TTS.api import TTS
from pydub import AudioSegment

logger = logging.getLogger('services')


class CoquiService:

    BLACKLISTED_MODELS = json.load(open("resources/BLACKLISTED_MODELS.json"))
    VC_MODEL = "tts_models/multilingual/multi-dataset/xtts_v2"

    def __init__(self):
        self.api = TTS()
        self.models = self.create_models_dict()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def create_models_dict(self) -> dict[ModelResponse]:
        models_dict = {}
        for model in self.api.list_models():
            if model not in self.BLACKLISTED_MODELS:
                self.api = TTS(model_name=model)
                [speakers, languages] = [
                    self.list_speakers(), self.list_languages()]
                models_dict[model] = ModelResponse(
                    is_multi_lingual=self.api.is_multi_lingual,
                    languages=languages.list,
                    is_multi_speaker=self.api.is_multi_speaker,
                    speakers=speakers.list
                )
        return models_dict

    def list_vc_speakers(self) -> ListResponse:
        with open("resources/created_models.json") as f:
            if os.stat("resources/created_models.json").st_size == 0:
                jsonData = []
            else:
                jsonData = json.load(f)

        speakers = [data["name"] for data in jsonData]
        return ListResponse(list=speakers)

    def list_models(self) -> ListResponse:
        return ListResponse(list=self.models.keys())

    def list_speakers(self) -> ListResponse:
        if self.api.is_multi_speaker:
            return ListResponse(list=self.api.speakers)
        else:
            return ListResponse(list=[])

    def list_languages(self) -> ListResponse:
        if self.api.is_multi_lingual:
            print(self.api.languages)
            return ListResponse(list=self.api.languages)
        else:
            return ListResponse(list=[])

    def get_model_info(self, request: str) -> ModelResponse:
        model_data: ModelResponse = self.models.get(request)
        return ModelResponse(
            is_multi_lingual=model_data.is_multi_lingual,
            languages=model_data.languages,
            is_multi_speaker=model_data.is_multi_speaker,
            speakers=model_data.speakers
        )

    def generate_audio(self, request: CoquiRequest) -> MessageResponse:
        self.api = TTS(model_name=request.model)
        # Generate random audio filename
        filename = str(uuid.uuid4()) + ".wav"
        filepath = "resources/outputs/" + filename
        self.api.tts_to_file(
            text=request.text,
            speaker=request.speaker if self.api.is_multi_speaker else None,
            language=request.language if self.api.is_multi_lingual else None,
            file_path=filepath
        )
        return MessageResponse(message=filename)

    def generate_speaker(self, request: CoquiCloneRequest) -> MessageResponse:
        try:
            base64_data = request.speaker_input.split(",")[-1]
            decoded_speaker_input = base64.b64decode(base64_data)
        except Exception as e:
            raise HTTPException(
                status_code=400, detail="El formato del audio no es válido.")

        filename = str(uuid.uuid4()) + ".webm"
        filepath = "resources/inputs/" + filename
        with open(filepath, "wb") as f:
            f.write(decoded_speaker_input)

        audio = AudioSegment.from_file(filepath, format="webm")
        audio = audio.set_sample_width(2)
        audio = audio.set_channels(2)
        audio = audio.set_frame_rate(48000)
        audio.export(filepath.replace(".webm", ".wav"), format="wav")
        os.remove(filepath)

        with open("resources/created_models.json") as f:
            if os.stat("resources/created_models.json").st_size == 0:
                jsonData = []
            else:
                jsonData = json.load(f)

        speaker_data = {
            "type": "voice-cloning",
            "name": request.speaker_name,
            "input": filepath.split(".")[0] + ".wav"
        }
        jsonData.append(speaker_data)
        self.models["tts_models/multilingual/multi-dataset/xtts_v2"].speakers.append(
            speaker_data["name"])

        with open("resources/created_models.json", "w") as f:
            json.dump(jsonData, f)

        return MessageResponse(message="Creación satisfactoria.")

    async def generate_cloning(self, request: CoquiRequest) -> MessageResponse:
        self.api = TTS(model_name=self.VC_MODEL)

        generated_speaker = json.load(open("resources/created_models.json"))

        for speaker in generated_speaker:
            if request.speaker in speaker["name"]:
                speaker_input = speaker["input"]
                speaker_selected = None
                break
            else:
                speaker_input = None
                speaker_selected = request.speaker

        output_filepath = "resources/outputs/" + str(uuid.uuid4()) + ".wav"
        params = {
            "text": request.text,
            "speaker_wav": speaker_input,
            "speaker": speaker_selected,
            "language": request.language,
            "file_path": output_filepath
        }

        if self.api.is_multi_lingual:
            params["language"] = request.language

        logger.info(params)

        self.api.tts_to_file(**params)

        return MessageResponse(message=output_filepath.split("/")[-1])

    async def generate(self, request: CoquiRequest) -> MessageResponse:
        if request.model is not None:
            return self.generate_audio(request)
        else:
            return await self.generate_cloning(request)

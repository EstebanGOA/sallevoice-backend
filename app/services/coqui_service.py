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

# Configure the logger
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CoquiService:

    blacklisted_models = ["tts_models/multilingual/multi-dataset/bark",
                          "tts_models/en/ljspeech/vits",
                          "tts_models/en/ljspeech/vits--neon",
                          "tts_models/en/ljspeech/overflow",
                          "tts_models/en/ljspeech/neural_hmm",
                          "tts_models/en/vctk/vits",
                          "tts_models/en/sam/tacotron-DDC",
                          "tts_models/en/blizzard2013/capacitron-t2-c50",
                          "tts_models/en/blizzard2013/capacitron-t2-c150_v2",
                          "tts_models/de/thorsten/tacotron2-DCA",
                          "tts_models/de/thorsten/tacotron2-DDC",
                          "tts_models/el/cv/vits",
                          "tts_models/ca/custom/vits",
                          "tts_models/fa/custom/glow-tts",
                          'vocoder_models/universal/libri-tts/wavegrad',
                          'vocoder_models/universal/libri-tts/fullband-melgan',
                          'vocoder_models/en/ek1/wavegrad',
                          'vocoder_models/en/ljspeech/multiband-melgan',
                          'vocoder_models/en/ljspeech/hifigan_v2',
                          'vocoder_models/en/ljspeech/univnet',
                          'vocoder_models/en/blizzard2013/hifigan_v2',
                          'vocoder_models/en/vctk/hifigan_v2',
                          'vocoder_models/en/sam/hifigan_v2',
                          'vocoder_models/nl/mai/parallel-wavegan',
                          'vocoder_models/de/thorsten/wavegrad',
                          'vocoder_models/de/thorsten/fullband-melgan',
                          'vocoder_models/de/thorsten/hifigan_v1',
                          'vocoder_models/ja/kokoro/hifigan_v1',
                          'vocoder_models/uk/mai/multiband-melgan',
                          'vocoder_models/tr/common-voice/hifigan',
                          'vocoder_models/be/common-voice/hifigan',
                          'voice_conversion_models/multilingual/vctk/freevc24']

    def __init__(self):
        self.api = TTS()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def list_models(self) -> ListResponse:
        models = []
        for model in self.api.list_models():
            if model in self.blacklisted_models:
                continue
            models.append(model)
        return ListResponse(list=models)

    # It cannot be called without initializing self.api with a model_name>
    def list_speakers(self) -> ListResponse:
        if self.api.is_multi_speaker:
            return ListResponse(list=self.api.speakers)
        else:
            return ListResponse(list=[])

    # It cannot be called without initializing self.api with a model_name
    def list_languages(self) -> ListResponse:
        if self.api.is_multi_lingual:
            print(self.api.languages)
            return ListResponse(list=self.api.languages)
        else:
            return ListResponse(list=[])

    def get_model_info(self, request: str) -> ModelResponse:
        self.api = TTS(model_name=request)
        [speakers, languages] = [self.list_speakers(), self.list_languages()]
        return ModelResponse(
            is_multi_lingual=self.api.is_multi_lingual,
            languages=languages.list,
            is_multi_speaker=self.api.is_multi_speaker,
            speakers=speakers.list
        )

    def generate_audio(self, request: CoquiRequest) -> MessageResponse:
        self.api = TTS(model_name=request.model)
        # Generate random audio filename
        filename = str(uuid.uuid4()) + ".wav"
        filepath = BASE_OUTPUT_PATH + filename
        self.api.tts_to_file(
            text=request.text,
            speaker=request.speaker if self.api.is_multi_speaker else None,
            language=request.language if self.api.is_multi_lingual else None,
            file_path=filepath
        )
        return MessageResponse(message=filename)

    async def generate_voice_cloning(self, request: CoquiRequest) -> MessageResponse:
        self.api = TTS(model_name=request.model)

        try: 
            base64_data = request.speaker_input.split(",")[-1]
            decoded_speaker_input = base64.b64decode(base64_data)
        except Exception as e: 
            raise HTTPException(status_code=400, detail="Invalid Base64 for speaker_input")
        
        input_filepath = BASE_INPUT_PATH + str(uuid.uuid4()) + ".webm"
        input_wav_filepath = BASE_INPUT_PATH + str(uuid.uuid4()) + ".wav"
        with open(input_filepath, "wb") as f:
            f.write(decoded_speaker_input)

        # Convert the input file to WAV format if necessary
        audio = AudioSegment.from_file(input_filepath, format="webm")
        audio = audio.set_sample_width(2)
        audio = audio.set_channels(2)
        audio = audio.set_frame_rate(48000)
        audio.export(input_wav_filepath, format="wav")

        # Delete the webm file
        os.remove(input_filepath)
        
        output_filepath = BASE_OUTPUT_PATH + str(uuid.uuid4()) + ".wav"
        params = {
            "text": request.text,
            "speaker_wav": input_wav_filepath,
            "language": request.language,
            "file_path": output_filepath
        }

        if self.api.is_multi_lingual:
            params["language"] = request.language

        logger.info(params)

        self.api.tts_to_file(**params)

        return MessageResponse(message=output_filepath.split("/")[-1])

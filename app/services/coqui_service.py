from . import *

import uuid
import torch
from TTS.api import TTS  # Example Coqui TTS model

class CoquiService: 
    
    BASE_OUTPUT_PATH = "resources/outputs/"
    BASE_INPUT_PATH = "resources/inputs/"
    
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

    def list_models(self):
        models = []
        for model in self.api.list_models():
            if model in self.blacklisted_models:
                continue
            models.append(model)
        return models

    # It cannot be called without initializing self.api with a model_name>
    def list_speakers(self): 
        if self.api.is_multi_speaker:
            return self.api.speakers
        else: 
            return []
    
    # It cannot be called without initializing self.api with a model_name
    def list_languages(self) -> list: 
        if self.api.is_multi_lingual:
            return self.api.languages
        else: 
            return []
    
    def get_model_info(self, request: str): 
        self.api = TTS(model_name=request)
        [speakers, languages] = [self.list_speakers(), self.list_languages()]
        model_info = {
            'is_multi_speaker': self.api.is_multi_speaker,
            'speakers': speakers,
            'is_multi_lingual': self.api.is_multi_lingual,
            'languages': languages
        }
        return model_info
        
    def generate_audio(self, request: CoquiRequest):
        self.api = TTS(model_name=request.model)
        # Generate random audio filename
        filename = str(uuid.uuid4()) + ".wav"
        filepath = self.BASE_OUTPUT_PATH + filename
        self.api.tts_to_file(
            request.text, 
            file_path=filepath
            )
        return filename
    
    # TODO: Se deben controlar los siguiente errores: 
    # - El archivo de audio no es un archivo WAV.
    # - Si el modelo es multilingual se debe pasar como parámetro el idioma. Por defecto será español. 
    # - Para saber los speaker que se pueden seleccionar de un modelo se puede usar el método tts_speakers()
    def generate_voice_cloning(self, request: CoquiRequest):
        self.api = TTS(model_name=request.model)

        inputFilepath = AudioService.save_file(in_file=request.speaker_input)

        params = {
            "text": request.text,
            "speaker_wav": inputFilepath,
            "language": request.language,
            "file_path": self.BASE_OUTPUT_PATH
        }
        
        if self.api.is_multi_lingual: 
            params["language"] = request.language
            
        self.api.tts_to_file(**params)
        
        return self.BASE_OUTPUT_PATH

import uuid
from . import *
import torchaudio

from speechbrain.inference.TTS import Tacotron2
from speechbrain.inference.vocoders import HIFIGAN


class SpeechBrainService:
    vocoders = [
        'speechbrain/tts-hifigan-ljspeech',
    ]

    models = [
        'speechbrain/tts-tacotron2-ljspeech'
    ]

    def __init__(self):
        pass

    def list_models(self):
        """TODO - Listar modelos disponibles. 
                Se descargan de la URL: https://huggingface.co/speechbrain/ hay que recoger la información de los modelos disponibles.
                Cada modelo tiene diferentes configuraciones y está preparado para diferentes tareas. Se debería seleccionar ciertos modelos para implementar. 
                Lo que implicaría no implementar todos los modelos disponibles, sino únicamente los que ofrezcan las funcionalidades que nos interesen. 
                """
        return ListResponse(list=self.models)
    
    def list_vocoders(self):
        return ListResponse(list=self.vocoders)

    def generate_audio(self, request: SpeechBrainRequest):
        # Intialize TTS (tacotron2) and Vocoder (HiFIGAN)
        tacotron2 = Tacotron2.from_hparams(source=request.tts, savedir="resources/tts")
        hifi_gan = HIFIGAN.from_hparams(
            source=request.vocoder, savedir="resources/vocoder")

        # Running the TTS
        mel_output, mel_length, alignment = tacotron2.encode_text(request.text)

        # Running Vocoder (spectrogram-to-waveform)
        waveforms = hifi_gan.decode_batch(mel_output)

        filepath = BASE_OUTPUT_PATH + str(uuid.uuid4()) + ".wav"
        torchaudio.save(filepath,
                        waveforms.squeeze(1), 22050)

        return MessageResponse(message=filepath.split("/")[-1])

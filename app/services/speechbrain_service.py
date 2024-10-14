import uuid
from . import *
import torchaudio

from speechbrain.inference.TTS import Tacotron2, MSTacotron2
from speechbrain.inference.vocoders import HIFIGAN

logger = logging.getLogger('services')

class SpeechBrainService:
    vocoders = [
        'speechbrain/tts-hifigan-ljspeech',
        'speechbrain/tts-hifigan-libritts-22050Hz'
    ]

    models = [
        'speechbrain/tts-tacotron2-ljspeech',
        'speechbrain/tts-mstacotron2-libritts'
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
        if (request.tts == 'speechbrain/tts-tacotron2-ljspeech'):
            model = Tacotron2.from_hparams(source=request.tts, savedir="resources/tts")
        elif (request.tts == 'speechbrain/tts-mstacotron2-libritts'):
            model = MSTacotron2.from_hparams(source=request.tts, savedir="resources/tts")

        hifi_gan = HIFIGAN.from_hparams(
            source=request.vocoder, savedir="resources/vocoder")

        if (request.tts == 'speechbrain/tts-tacotron2-ljspeech'):
            mel_output, mel_length, alignment = model.encode_text(request.text)
        elif (request.tts == 'speechbrain/tts-mstacotron2-libritts'):
            mel_output, mel_length, alignment = model.generate_random_voice(request.text)

        waveforms = hifi_gan.decode_batch(mel_output)

        filepath = "resources/outputs/" + str(uuid.uuid4()) + ".wav"
        torchaudio.save(filepath,
                        waveforms.squeeze(1), 22050)

        return MessageResponse(message=filepath.split("/")[-1])

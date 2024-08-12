import torchaudio

from speechbrain.inference.TTS import Tacotron2
from speechbrain.inference.vocoders import HIFIGAN

class SpeechBrainService: 
    def __init__(self):
        pass
    
    def list_models(self): 
        """TODO - Listar modelos disponibles. 
                Se descargan de la URL: https://huggingface.co/speechbrain/ hay que recoger la información de los modelos disponibles.
                Cada modelo tiene diferentes configuraciones y está preparado para diferentes tareas. Se debería seleccionar ciertos modelos para implementar. 
                Lo que implicaría no implementar todos los modelos disponibles, sino únicamente los que ofrezcan las funcionalidades que nos interesen. 
                """
        return {
            'vocoder': [
                'speechbrain/tts-hifigan-ljspeech',
            ],
            'speaker': [
                'speechbrain/tts-tacotron2-ljspeech'
            ]
        }
         
    
    def generate_audio(self, tts: str, vocoder: str, text: str): 
        # Intialize TTS (tacotron2) and Vocoder (HiFIGAN)
        tacotron2 = Tacotron2.from_hparams(source=tts, savedir="tmpdir_tts")
        hifi_gan = HIFIGAN.from_hparams(source=vocoder, savedir="tmpdir_vocoder")
        
        # Running the TTS
        mel_output, mel_length, alignment = tacotron2.encode_text(text)
        
        # Running Vocoder (spectrogram-to-waveform)
        waveforms = hifi_gan.decode_batch(mel_output)
        
        torchaudio.save('resources/outputs/output.wav', waveforms.squeeze(1), 22050)
        
        return 'resources/outputs/output.wav'
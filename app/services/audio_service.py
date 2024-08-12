from . import *

import os
import aiofiles

class AudioService:
    def get_audio_filenames(self): 
        return [f for f in os.listdir("resources/outputs") if os.path.isfile(os.path.join("resources/outputs", f))]
    
    def get_audio_by_filename(self, filename): 
        """Recoge la ruta de un archivo de audio a partir de su nombre. 

        Args:
            filename (_type_): Nombre del archivo de audio.

        Returns:
            _type_: Ruta del archivo de audio.
        """
        return os.path.join("resources/outputs", filename)
    
    async def save_file(in_file: UploadFile = File(...), out_file_path: str = "resources/inputs/input.wav"):
        """Guarda un archivo en disco a partir de un archivo subido. 

        Args:
            in_file (UploadFile, optional): Archivo de audio subido. Defaults to File(...).
            out_file_path (str, optional): Nombre del archivo de audio. Defaults to "resources/inputs/input.wav".

        Returns:
            _type_: _description_
        """
        async with aiofiles.open(out_file_path, 'wb') as out_file:
            content = await in_file.read()
            await out_file.write(content)
        return out_file.name
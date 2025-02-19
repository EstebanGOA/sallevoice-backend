from . import *

import os
import aiofiles

logger = logging.getLogger('services')

class AudioService:
    def get_audio_filenames(self) -> list[str]:
        return [f for f in os.listdir("resources/outputs") if os.path.isfile(os.path.join("resources/outputs", f))]

    def get_audio_by_filename(self, filename: str) -> str:
        """Recoge la ruta de un archivo de audio a partir de su nombre. 

        Args:
            filename (_type_): Nombre del archivo de audio.

        Returns:
            _type_: Ruta del archivo de audio.
        """
        return MessageResponse(message=os.path.join("resources/outputs", filename))

    async def save_file(in_file: bytes, out_file_path: str) -> str:
        """Guarda un archivo en disco a partir de un archivo subido. 

        Args:
            in_file (UploadFile): Archivo de audio subido.
            out_file_path (str): Nombre del archivo de audio.

        Returns:
            _type_: _description_
        """
        async with aiofiles.open(out_file_path, 'wb') as out_file:
            await out_file.write(in_file)
        return out_file.name

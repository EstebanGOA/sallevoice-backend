from . import *

from contextlib import closing
import os
from tempfile import gettempdir
import uuid

from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from fastapi import HTTPException

logger = logging.getLogger('services')


class PollyService():

    def __init__(self):
        self.client = Session(
            aws_access_key_id="AKIATNVEV3B5WKWUK47C",
            aws_secret_access_key="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",
            region_name="us-east-1"
        ).client("polly")

    def speech_synthesis(self, request: PollyRequest):
        try:
            response = self.client.synthesize_speech(
                OutputFormat="mp3",
                **request.model_dump()
            )
        except (BotoCoreError, ClientError) as error:
            logger.info(error)
            raise HTTPException(
                status_code=400, detail="Error al conectar con el servicio de AWS Polly.")

        logger.info(response)
        if "AudioStream" in response:
            with closing(response["AudioStream"]) as stream:
                filename = str(uuid.uuid4()) + ".wav"
                output = os.path.join("resources/outputs/", filename)
                try:
                    with open(output, "wb") as file:
                        file.write(stream.read())
                except IOError as error:
                    logger.info(error)
                    raise HTTPException(
                        status_code=400, detail="Error al guardar el archivo de audio.")
        else:
            logger.info("No se recibió un archivo de audio.")
            raise HTTPException(
                status_code=400, detail="No se recibió un archivo de audio.")

        return filename

    def list_voices(self, request: PollyVoiceRequest) -> PollyVoiceResponse:
        try:
            response = self.client.describe_voices(**request.model_dump())
            return PollyVoiceResponse(Voices=response["Voices"])
        except (self.client.exceptions.InvalidNextTokenException, self.client.exceptions.ServiceFailureException) as error:
            logger.info(error)
            raise HTTPException(
                status_code=400, detail="Se ha producido un error al actualizar las voces disponibles.")
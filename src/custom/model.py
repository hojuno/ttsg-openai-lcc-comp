'''
Class implementing TTS generation using OpenAI TTS service.
'''

from dotenv import load_dotenv
load_dotenv()
import openai

with openai.audio.speech.with_streaming_response.create(
    model="tts-1",
    voice="alloy",
    response_format="pcm",  # similar to WAV, but without a header chunk at the start.
    input="""I see skies of blue and clouds of white
            The bright blessed days, the dark sacred nights
            And I think to myself
            What a wonderful world""",
) as response:
    for chunk in response.iter_bytes(chunk_size=1024):
        print(chunk)

from openai import OpenAI
import logging

class OpenAITTSModel():
    def __init__(self, model_name, voice_name):
        self.model_name = model_name
        self.voice_name = voice_name

    def __call__(self, content: str):
        logging.debug(f"Generating OpenAI TTS response stream for message: {content}")
        with openai.audio.speech.with_streaming_response.create(
            model=self.model_name,
            voice=self.voice_name,
            response_format="pcm",  # similar to WAV, but without a header chunk at the start.
            input=content
        ) as response:
            for chunk in response.iter_bytes(chunk_size=4096):
                yield chunk
        logging.debug("Finished generating response.")
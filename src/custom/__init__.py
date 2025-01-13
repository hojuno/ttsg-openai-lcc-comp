'''
Supported component type entrypoints

- Implement the specific entrypoint associated with your component type
- You can leave the others unimplemented

To support streaming, your implementation should be a generator: https://wiki.python.org/moin/Generators
You may also simply return the final result
'''

import os
from .model import OpenAITTSModel
ttsg_model = OpenAITTSModel(os.getenv('MODEL'), os.getenv('VOICE'))

# For speech-to-text models
def start_stt(audio: bytes) -> str:
    raise NotImplementedError

# For text generation models
def start_t2t(system_prompt: str, user_input: str) -> str:
    raise NotImplementedError

# For text-to-speech generation
def start_ttsg(text: str) -> bytes:
    global ttsg_model
    for audio_chunk in ttsg_model(text):
        yield audio_chunk

# For voice changers
def start_ttsc(audio: bytes) -> bytes:
    raise NotImplementedError
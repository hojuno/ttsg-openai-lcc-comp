import openai
import logging

class OpenAITTSModel:
    def __init__(self, model_name, voice_name, client, translation_model="gpt-4o-mini"):
        self.model_name = model_name
        self.voice_name = voice_name
        self.client = client  # OpenAI 클라이언트 인스턴스
        self.translation_model = translation_model

    async def __call__(self, content: str):
        logging.debug(f"Translating input text to Korean: {content}")

        # 1. 입력 텍스트를 한국어로 번역
        translation_response = await self.client.chat.completions.acreate(
            model=self.translation_model,
            messages=[
                {"role": "system", "content": "You are a helpful translator."},
                {"role": "user", "content": f"Translate this text to Korean: {content}"}
            ]
        )
        translated_text = translation_response.choices[0].message.content.strip()
        logging.debug(f"Translated text: {translated_text}")

        # 2. 번역된 한국어 텍스트로 TTS 생성
        logging.debug(f"Generating OpenAI TTS response stream for message: {translated_text}")
        response = await self.client.audio.speech.create(
            model=self.model_name,
            voice=self.voice_name,
            response_format="pcm",
            input=translated_text
        )
        async for chunk in response.iter_bytes(chunk_size=4096):
            yield chunk
        logging.debug("Finished generating response.")

from providers.base import BaseAIProvider
from config import OPENAI_API_KEY
import openai

class OpenAIProvider(BaseAIProvider):
    def __init__(self):
        if OPENAI_API_KEY:
            openai.api_key = OPENAI_API_KEY

    async def generate_image(self, prompt: str) -> str:
        response = await openai.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        return response.data[0].url

    async def generate_video(self, prompt: str, image_path: str = None, duration: int = 5) -> str:
        raise NotImplementedError("OpenAI video API provider endpoint required.")

from providers.base import BaseAIProvider
from config import GEMINI_API_KEY

class GeminiProvider(BaseAIProvider):
    def __init__(self):
        self.api_key = GEMINI_API_KEY

    async def generate_image(self, prompt: str) -> str:
        # Mock adapter endpoint wrapper for Gemini Imagen API call
        return "https://via.placeholder.com/1024.png?text=Gemini+Generated+Image"

    async def generate_video(self, prompt: str, image_path: str = None, duration: int = 5) -> str:
        # Mock adapter endpoint wrapper for Gemini Video Generation workflow
        return "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4"

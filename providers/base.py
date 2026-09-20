from abc import ABC, abstractmethod

class BaseAIProvider(ABC):
    @abstractmethod
    async def generate_image(self, prompt: str) -> str:
        """Returns URL or local file path to generated image."""
        pass

    @abstractmethod
    async def generate_video(self, prompt: str, image_path: str = None, duration: int = 5) -> str:
        """Returns URL or local file path to generated video."""
        pass

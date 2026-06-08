import os
import yaml
from dotenv import load_dotenv
from modules.image_generator import ImageGenerator
from modules.video_generator import VideoGenerator
from modules.post_generator import PostGenerator
from modules.pinterest_uploader import PinterestUploader

# Загружаем переменные окружения
load_dotenv()

# Загружаем конфиг
with open('../config/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

class PinterestAgent:
    def __init__(self):
        self.image_gen = ImageGenerator()
        self.video_gen = VideoGenerator()
        self.post_gen = PostGenerator()
        self.uploader = PinterestUploader()
    
    def generate_content(self):
        """Генерирует фото, видео и посты"""
        print("🚀 Запускаем генерацию контента...")
        
        # Генерируем изображения
        print("📸 Генерирую изображения...")
        images = self.image_gen.generate()
        
        # Генерируем видео
        print("🎬 Генерирую видео...")
        videos = self.video_gen.generate()
        
        # Генерируем посты
        print("✍️ Генерирую посты...")
        posts = self.post_gen.generate(images, videos)
        
        return images, videos, posts
    
    def upload_to_pinterest(self, images, videos, posts):
        """Загружает контент в Pinterest"""
        print("📤 Загружаю контент в Pinterest...")
        self.uploader.upload(images, videos, posts)
        print("✅ Контент успешно загружен!")
    
    def run(self):
        """Запускает полный цикл агента"""
        images, videos, posts = self.generate_content()
        self.upload_to_pinterest(images, videos, posts)

if __name__ == "__main__":
    agent = PinterestAgent()
    agent.run()

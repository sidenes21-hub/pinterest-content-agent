import os
from openai import OpenAI
from datetime import datetime
import requests

class ImageGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "dall-e-3"
        self.output_dir = "../../data/generated/images"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate(self, prompt=None, count=3):
        """Генерирует изображения для Pinterest"""
        print(f"🎨 Генерирую {count} изображений...")
        
        if not prompt:
            prompt = "Beautiful Pinterest-style flat lay photography with modern aesthetic, trending on Pinterest 2024"
        
        images = []
        
        for i in range(count):
            try:
                response = self.client.images.generate(
                    model=self.model,
                    prompt=f"{prompt} - variation {i+1}",
                    size="1024x1024",
                    quality="hd",
                    n=1
                )
                
                image_url = response.data[0].url
                
                # Скачиваем изображение
                img_data = requests.get(image_url).content
                
                # Сохраняем локально
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{self.output_dir}/image_{timestamp}_{i}.png"
                
                with open(filename, 'wb') as f:
                    f.write(img_data)
                
                images.append({
                    'path': filename,
                    'url': image_url,
                    'prompt': prompt
                })
                
                print(f"✅ Изображение {i+1} создано: {filename}")
            
            except Exception as e:
                print(f"❌ Ошибка при генерации изображения {i+1}: {e}")
        
        return images

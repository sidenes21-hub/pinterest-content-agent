import os
import requests
from datetime import datetime

class PinterestUploader:
    def __init__(self):
        self.api_key = os.getenv("PINTEREST_API_KEY")
        self.api_secret = os.getenv("PINTEREST_API_SECRET")
        self.access_token = os.getenv("PINTEREST_ACCESS_TOKEN")
        self.base_url = "https://api.pinterest.com/v5"
    
    def upload(self, images, videos, posts):
        """Загружает контент в Pinterest"""
        print("📤 Начинаю загрузку контента в Pinterest...\n")
        
        for i, post in enumerate(posts):
            try:
                self._create_pin(post)
                print(f"✅ Пин {i+1} успешно загружен в Pinterest")
            except Exception as e:
                print(f"❌ Ошибка при загрузке пина {i+1}: {e}")
    
    def _create_pin(self, post):
        """Создает пин в Pinterest"""
        if not self.access_token:
            print("⚠️  Pinterest Access Token не установлен. Используется демо режим.")
            self._save_locally(post)
            return
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        media_path = post.get('media', {}).get('path', None)
        
        data = {
            "title": post['text'][:100],
            "description": post['text'],
            "link": "https://your-website.com",
            "board_id": "YOUR_BOARD_ID"
        }
        
        # Если есть изображение, загружаем с медиа
        if media_path and os.path.exists(media_path):
            with open(media_path, 'rb') as f:
                files = {'image': f}
                response = requests.post(
                    f"{self.base_url}/pins",
                    headers=headers,
                    data=data,
                    files=files,
                    timeout=30
                )
        else:
            response = requests.post(
                f"{self.base_url}/pins",
                headers=headers,
                json=data,
                timeout=30
            )
        
        if response.status_code not in [200, 201]:
            print(f"Pinterest API Response: {response.text}")
    
    def _save_locally(self, post):
        """Сохраняет пост локально (для демо)"""
        log_dir = "../../logs"
        os.makedirs(log_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{log_dir}/post_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Pinterest Post\n")
            f.write(f"==============\n")
            f.write(f"Timestamp: {post['timestamp']}\n")
            f.write(f"Media: {post.get('media', {}).get('path', 'None')}\n\n")
            f.write(f"Text:\n{post['text']}\n")

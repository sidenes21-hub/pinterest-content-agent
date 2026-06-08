import os
from openai import OpenAI
from datetime import datetime

class PostGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4"
    
    def generate(self, images, videos, count=3):
        """Генерирует текст постов для Pinterest"""
        print(f"✍️ Генерирую {count} постов...")
        
        posts = []
        
        prompts = [
            "Создай привлекательный пост для Pinterest про lifestyle и дизайн интерьера",
            "Создай пост про DIY и handmade для Pinterest с хештегами",
            "Создай пост про fashion и стиль жизни для Pinterest"
        ]
        
        for i in range(count):
            try:
                prompt = prompts[i % len(prompts)]
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "Ты эксперт в создании контента для Pinterest. Пишешь привлекательные посты с хештегами, эмодзи и call-to-action."
                        },
                        {
                            "role": "user",
                            "content": f"{prompt}\n\nДелай пост не более 500 символов. Добавь 5-10 релевантных хештегов."
                        }
                    ],
                    temperature=0.7,
                    max_tokens=500
                )
                
                post_text = response.choices[0].message.content
                
                # Выбираем изображение или видео для поста
                media = None
                if i < len(images):
                    media = images[i]
                elif i < len(videos):
                    media = videos[i - len(images)]
                
                post = {
                    'text': post_text,
                    'media': media,
                    'timestamp': datetime.now().isoformat()
                }
                
                posts.append(post)
                print(f"✅ Пост {i+1} создан")
                print(f"📝 {post_text[:100]}...\n")
            
            except Exception as e:
                print(f"❌ Ошибка при генерации поста {i+1}: {e}")
        
        return posts

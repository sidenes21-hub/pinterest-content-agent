import os
from moviepy.editor import *
from datetime import datetime

class VideoGenerator:
    def __init__(self):
        self.output_dir = "../../data/generated/videos"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate(self, count=2):
        """Генерирует видео для Pinterest"""
        print(f"🎥 Генерирую {count} видео...")
        
        videos = []
        
        try:
            for i in range(count):
                # Создаем простое видео с текстом
                duration = 5  # 5 секунд
                fps = 24
                
                # Черный фон
                clip = ColorClip(
                    size=(1080, 1920),
                    color=(0, 0, 0)
                ).set_duration(duration)
                
                # Добавляем текст
                txt_clip = TextClip(
                    f"Pinterest Content #{i+1}",
                    fontsize=70,
                    color='white',
                    font='Arial-Bold'
                ).set_position('center').set_duration(duration)
                
                # Объединяем
                final_clip = CompositeVideoClip([clip, txt_clip])
                
                # Сохраняем
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{self.output_dir}/video_{timestamp}_{i}.mp4"
                
                final_clip.write_videofile(
                    filename,
                    fps=fps,
                    verbose=False,
                    logger=None
                )
                
                videos.append({
                    'path': filename,
                    'duration': duration
                })
                
                print(f"✅ Видео {i+1} создано: {filename}")
            
        except Exception as e:
            print(f"❌ Ошибка при генерации видео: {e}")
        
        return videos

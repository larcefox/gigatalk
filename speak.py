from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
from io import BytesIO
import loguru
import sys
import os


# Настройка глобального уровня логирования
loguru.logger.level("INFO")
# Настройка формата вывода логов
logger = loguru.logger
logger.add(sys.stderr, format="{time} {level} {message}", filter="", backtrace=True, diagnose=True)

class PlaySound():
    def __init__(self) -> None:
        # pydub add to env
        os.environ["FFMPEG"] = "C:\\Users\\larce\\projects\\gigatalk\\ffmpeg\\bin"
        self.language = 'ru'
        self.voice_id = 'ru-RU-Standard-D'

    def save_audio(self, text) -> BytesIO:
        logger.info("Создаем аудио файл ответа.")
        answer = BytesIO()
        talker = gTTS(text=text, lang=self.language, slow=False)

        # Запись аудиофайла
        try:
            talker.write_to_fp(answer)
            answer.seek(0)
            return answer
        
        except gTTS.gTTSError as e:
            print(e)
            print("Невоспроизводимые символы в ответе.")
            return False
        
    def play_sound(self, sound) -> None:
        logger.info("Проигрываем ответ.")
        song = AudioSegment.from_file(sound, format="mp3")
        play(song)
  
if __name__ == "__main__":
    
    recognizer = VoiceRecognition()
    play_sound = PlaySound()
    
    play_sound.play_sound(recognizer.ready_sound)    
    query = recognizer.recognition()

    file = play_sound.save_audio(query)
    play_sound.play_sound(file)
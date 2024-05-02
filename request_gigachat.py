import os
from dotenv import load_dotenv
from requests import request as rq
from datetime import datetime as dt
import json
import loguru
import sys


# Настройка глобального уровня логирования
loguru.logger.level("INFO")
# Настройка формата вывода логов
logger = loguru.logger
logger.add(sys.stderr, format="{time} {level} {message}", filter="", backtrace=True, diagnose=True)


# Путь к файлу .env
env_file_path = '.env'

# Загрузка переменных окружения из файла .env
load_dotenv(dotenv_path=env_file_path)

class GigaChat():
    def __init__(self) -> None:
        self.RqUID = os.getenv('RqUID')
        self.Authorization = os.getenv('Authorization')
        self.auth_url =  os.getenv('AuthURL')
        self.payload = os.getenv('PAYLOAD')
        self.token_detail = None
        self.query_url = os.getenv('GigaURL')

    def request_token(self) -> str|bool:
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': self.RqUID,
        'Authorization': f'Basic {self.Authorization}'
        }

        try:
            response = rq("POST", self.auth_url, headers=headers, data=self.payload, verify=False)
        except ConnectionError as conn_error:
            print(conn_error)
            response = False

        if response.status_code == 200:
            logger.info("Создан токен.")
            return response.json()
        else:
            logger.info("Ошибка создания токена.")
            return False
        
    def get_token(self) -> str:
        if self.token_detail:
            logger.info(f'Сравнение дат: {dt.now()}, {dt.fromtimestamp(self.token_detail['expires_at'] / 1000)}')
            if dt.now() < dt.fromtimestamp(self.token_detail['expires_at'] / 1000):
                logger.info("Токен действителен.")
                return self.token_detail['access_token']
            else:
                logger.info("Токен просрочен, получаем новый.")
                self.token_detail = self.request_token()
                return self.token_detail['access_token']
        else:
            logger.info("Нет токена")
            self.token_detail = self.request_token()
            return self.token_detail['access_token']

    def send_prompt(self, token, prompt) -> str:
        
        logger.info(f"Запрос к Гигачат: {prompt}")
                
        if prompt == 'выход':
            logger.info("Выход по команде.")
            exit(0)
            
        payload = json.dumps({
        "model": "GigaChat",
        "messages": [
            {
            "role": "user",
            "content": prompt
            }
        ],
        "temperature": 1,
        "top_p": 0.1,
        "n": 1,
        "stream": False,
        "max_tokens": 512,
        "repetition_penalty": 1
        })
        headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}'
        }
        logger.info("Отправка запроса.")
        try:        
            response = rq("POST", self.query_url, headers=headers, data=payload, verify=False)
            answer = response.json()['choices'][0]['message']['content']
            logger.info(f"Ответ получен: {answer}")
            return answer
        except ConnectionError as conn_error:
            print(conn_error)
            logger.info("Ошибка отправки запроса.")

if __name__ == '__main__':
    gigachat = GigaChat()
    token = gigachat.get_token()
    gigachat.send_prompt(token, 'Как тебя зовут?')

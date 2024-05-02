For running script you need to add .env file with following params:

RqUID = ""
Authorization = ""
GigaURL = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
AuthURL = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
PAYLOAD = 'scope=GIGACHAT_API_PERS'


RqUID and Authorization you can get on https://developers.sber.ru
It requires to register by phone number or SberID.

Also you can have troubles with ffmpeg, I ran it on Windows, for Linux it needs to adopt.
FFMPEG to download - https://ffmpeg.org/download.html

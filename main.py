from listen import VoiceRecognition
from request_gigachat import GigaChat
from speak import PlaySound


if __name__ == '__main__':

    recognizer = VoiceRecognition()
    play_sound = PlaySound()
    chat = GigaChat()

    while True:
        if recognizer.word_check(recognizer.recognition()):
            play_sound.play_sound(recognizer.ready_sound)
            query = recognizer.recognition()
        else:
            continue


        token = chat.get_token()
        answer = chat.send_prompt(token, query)
        
        file = play_sound.save_audio(answer)
        play_sound.play_sound(file)
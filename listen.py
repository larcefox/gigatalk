import speech_recognition as sr


class VoiceRecognition():
    def __init__(self, device_index=0) -> None:
        
        # index of recording device
        self.device_index = device_index
        
        # Creation of reconition object
        self.rercognizer = sr.Recognizer()
        
        # Recognized text
        self.text = None
        
        # Play sound
        self.ready_sound = "ready.mp3"
        
        # Playback object
        self.playback = None

    def recognition(self) -> str:

        # Захват аудио с микрофона
        with sr.Microphone(self.device_index) as source:
            audio = self.rercognizer.listen(source)
        
        # Преобразование аудио в текст
        try:
            # Преобразование речи в текст с использованием Google Speech-to-Text
            self.text = self.rercognizer.recognize_google(audio, language="ru-RU")
            return self.text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio.")
        except sr.RequestError as e:
            print("Could not request Google Speech Recognition service; {0}".format(e))
            
    def list_devices(self):
        # List known record devices
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
            
    def word_check(self, text):
        text = self.recognition()
        if text and 'гигачад' in text:
            return True
        else:
            return False

        
if __name__ == '__main__':
    pass
import threading
import time

import pyttsx3
# import simpleaudio as sa

class alertThread (threading.Thread):
    def __init__(self, threadID=1, name='音频线程', text=None):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.text = text
    
    def run(self):
        """
        有字说字，没字播 wav
        """
        if self.text:
            self.play_text()
        else:
            self.play_sound()

    def play_sound(self):
        """
        播放提示音
        """
        # wave_obj = sa.WaveObject.from_wave_file('alert.wav')
        # play_obj = wave_obj.play()
        # play_obj.wait_done()
        pass
    
    def play_text(self):
        """
        文字转语音
        """
        # text='咪咕读书打卡完毕'
        voice=pyttsx3.init()
        # linux 下 pyttsx3 以来 espeak 库，但是声线太 low 了，说英语还凑合
        # voice.setProperty('voice', 'zh')
        voice.say(self.text)
        voice.runAndWait()

if __name__ == "__main__":
    a = alertThread(1, text='mission complete')
    a.start()
    pass
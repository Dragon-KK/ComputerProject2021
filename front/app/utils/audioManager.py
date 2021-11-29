import webbrowser

class Audio:
    def __init__(self):
        pass

    def PlayAsync(self):
        pass

    def Play(self):
        pass

    def Status(self):
        pass

class AudioManager:
    def __init__(self):
        pass

    def LoadAudioFile(self):
        pass

    def ClearAll(self):
        pass

    

 
bgmusic = r"C:\Users\kaush\OneDrive\Documents\GitHub\Comp Project\ComputerProject2021\front\app\media\Audio\AdhesiveWombat - Night Shade.mp3"
from pydub import AudioSegment 
from pydub.playback import play 
import pydub
  
# Import an audio file 
# Format parameter only
# for readability 
wav_file = AudioSegment.from_file(file = bgmusic, 
                                  format = "mp3") 
x = pydub.playback._play_with_simpleaudio(wav_file.fade_in(10))
x.wait_done()
# Play the audio file
# play(wav_file)
wav_file.reverse()
play(wav_file.reverse())
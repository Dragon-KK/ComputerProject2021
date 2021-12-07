import pydub
from pathlib import Path
from random import choice
from pydub.playback import _play_with_simpleaudio as play

AUDIO_DIR = Path(__file__).parent.parent.joinpath('media/Audio')

class audioFiles:
    jump = AUDIO_DIR.joinpath("Bounce.wav")
    
    @staticmethod
    def GetRandomBackgroundMusic():
        return AUDIO_DIR.joinpath(choice(["BG1.mp3"]))

class Player:
    def __init__(self, audio, Async = False):
        self.object = play(audio)

    def IsPlaying(self):
        return self.object.is_playing()

    def Stop(self):
        self.object.stop()

class Audio(pydub.AudioSegment):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.Players = []
        
    def PlayAsync(self, keepTrack = False):
        player = Player(self,print)
        if keepTrack:self.Players.append(player)
        return player

    def EndAllPlayers(self):
        for player in self.Players:
            player.Stop()

class AudioManager:
    def __init__(self):
        self.Audios = []

    def LoadAudio(self,filepath):
        audio = Audio.from_file(filepath)
        self.Audios.append(audio)
        return audio

    def EndAll(self):
        for audio in self.Audios:
            audio.EndAllPlayers()

class PongAudioManager(AudioManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.bgMusicIsPlaying = False
    def startBGMusic(self):
        self.bgMusicIsPlaying = True
        self.LoadAudio(audioFiles.GetRandomBackgroundMusic()).PlayAsync(keepTrack=True)
    def stopBGMusic(self):
        self.bgMusicIsPlaying = False
        self.EndAll()



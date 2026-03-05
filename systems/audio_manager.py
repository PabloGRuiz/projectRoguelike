import pygame

class AudioManager:
    def __init__(self):
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        self.current_music = None

    def play_music(self, path, loop=True, volume=0.5):
        if self.current_music != path:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1 if loop else 0)
            self.current_music = path

    def stop_music(self):
        pygame.mixer.music.stop()
        self.current_music = None

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)
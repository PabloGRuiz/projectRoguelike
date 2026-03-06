import sys
import os

if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

from core.game import Game

if __name__ == "__main__":
    Game().run()
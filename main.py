import multiprocessing
from ui import UIController
from audio import AudioPlayer
from api import HttpManager
from game import GameManager

#Start the Program
if __name__ == "__main__":
    # Pyinstaller fix
    multiprocessing.freeze_support()
    ui = UIController()
    httpManager = HttpManager()
    audioPlayer = AudioPlayer()
    gameManager = GameManager(ui)
    print('> starting tkinter')
    ui.Start()

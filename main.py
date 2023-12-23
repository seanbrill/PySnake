from ui import UIController
from audio import AudioPlayer
from api import HttpManager
from game import GameManager

#Start the Program
if __name__ == "__main__":
    ui = UIController()
    httpManager = HttpManager()
    audioPlayer = AudioPlayer()
    gameManager = GameManager(ui)
    ui.Start()

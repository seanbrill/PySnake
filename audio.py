import winsound
from multiprocessing import Process, Manager

class AudioPlayer:

    instance: 'AudioPlayer' = None
    processes = []
    active_sounds : Manager = None

    def __init__(self):
        AudioPlayer.instance = self
        manager = Manager()
        AudioPlayer.active_sounds = manager.list('')
        # prime the audio player
        self.Play('./assets/audio/blank.wav')
        self.Play('./assets/audio/blank.wav')
        

    def _play_(self, file_path, sound_tag = None, active_sounds = None):
            winsound.PlaySound(file_path, 0)
            # remove it from active sounds if it was not null
            if sound_tag != None and active_sounds != None:
               active_sounds.remove(sound_tag)

    def Play(self, file_path, sound_tag = None):
        if sound_tag == None:
            proc = Process(target=self._play_, args=(file_path,None,None))
            proc.start()
            AudioPlayer.processes.append(proc)
        # if sound restriction pass memory address to subprocess
        elif (sound_tag not in AudioPlayer.active_sounds):
            AudioPlayer.active_sounds.append(sound_tag)
            proc = Process(target=self._play_, args=(file_path, sound_tag, self.active_sounds))
            proc.start()
            AudioPlayer.processes.append(proc)
        else:
            pass

    def StopAll(self):
        for process in AudioPlayer.processes:
            process.terminate()
        # Clear the list by slicing it
        AudioPlayer.active_sounds[:] = []
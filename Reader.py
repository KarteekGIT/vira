import threading as mp
import pygame
class Reader(object):
    def __init__(self, filename):
        self.filename = filename
        self.flag = False
        self.running_process=[]
        pygame.mixer.init()
        pygame.mixer.music.load(self.filename)        
        
    def reading(self):
        print("Reader started")
        pygame.mixer.music.play() 
        print("Done")
                
    def play_or_stop(self):
        while pygame.mixer.music.get_busy():
            fileOpen = open("buttons/stop", "r+")
            fileOpen2 = open("buttons/play", "r+")
            play = fileOpen2.read(5)
            stop = fileOpen.read(5)
            play = play.strip("\n")
            stop = stop.strip("\n")            
            if(stop == "True"):
                self.flag = True
            if(play == "True"):
                print("play")
                fileOpen2.seek(0)
                fileOpen2.write('False')
                print("Write False to play")
                fileOpen2.truncate()
                fileOpen2.close()
                pygame.mixer.music.unpause()

            while self.flag:
                if(stop == "True"):
                    print("stop")
                    self.flag = False
                    fileOpen.seek(0)
                    fileOpen.write('False')
                    print("Write False to stop")
                    fileOpen.truncate()
                    fileOpen.close()
                    pygame.mixer.music.pause()

    def rewind(self):
        while pygame.mixer.music.get_busy():
            fileOpen = open("buttons/rewind")
            rewind = fileOpen.read(5)
            if(rewind == "True"):
                print("rewind")
                pygame.mixer.music.rewind()
                fileOpen.seek(0)
                fileOpen.write("False")
                fileOpen.truncate()
                fileOpen.close()

                
    def go(self):
        print("Ready for reading")
        reading = mp.Thread(target=self.reading, name="reading process")
        playing = mp.Thread(target=self.play_or_stop, name="process waiting for play")
        rewind = mp.Thread(target=self.rewind, name="process waiting for rewind")        
        reading.start()
        playing.start()
        rewind.start()
        print("Process for play stop rewind started")
        self.running_process.append(playing)
        self.running_process.append(rewind)
        self.running_process.append(reading)    
        for proc in self.running_process:
            if proc.is_alive():
                proc.join()        
import time
import pygame


#音乐路径

filePath = "D:\\"

#初始化
pygame.mixer.init()
#加载音乐
track = pygame.mixer.music.load(filePath)
#播放
pygame.mixer.music.play()
#
time.sleep(10)
pygame.mixer.music
#停止
pygame.mixer.music.stop()


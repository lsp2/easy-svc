import pygame
import os
import time

#控制音频播放

class AudioPlayer:
    def __init__(self, file_path):
        pygame.init()
        pygame.mixer.init()
        self.file_path = file_path
        self.is_playing = False
        self.current_position = 0

    #导入本地音乐
    def load_audio(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        pygame.mixer.music.load(self.file_path)

    #播放音乐
    def play(self):
        if not self.is_playing:
            self.load_audio()
            pygame.mixer.music.play(start=self.current_position)
            self.is_playing = True

    #暂停播放
    def pause(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
            self.current_position = pygame.mixer.music.get_pos() // 1000  # Convert milliseconds to seconds
   
    #终止播放
    def stop(self):
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False
            self.current_position = 0
    
    #跳转时长
    def jump_to(self, seconds):
        if self.is_playing:
            pygame.mixer.music.stop()
        self.current_position = seconds
        self.play()

    #获取总时长（s）
    def get_duration(self):
        sound = pygame.mixer.Sound(self.file_path)
        return sound.get_length()
    
    #获取当前播放时长（s）
    def get_current_position(self):
        if self.is_playing:
            return pygame.mixer.music.get_pos() // 1000  # Convert milliseconds to seconds
        else:
            return self.current_position
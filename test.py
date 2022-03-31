import pygame
import ctypes
from pygame.locals import *
from color import Color

class Test():
    def __init__(self):
        ctypes.windll.user32.SetProcessDPIAware()
        self.width = ctypes.windll.user32.GetSystemMetrics(0)
        self.height = ctypes.windll.user32.GetSystemMetrics(1)
        self.window = pygame.display.set_mode((self.width, self.height))#, pygame.FULLSCREEN)
        
        self.bt_red = self.bt_yellow = self.bt_green = self.bt_blue = self.bt_orange = None
        self.bt_pink = self.bt_brown = self.bt_black = self.bt_white = self.bt_purple = None
        self.bt_largerBrush = self.bt_smallerBrush = self.bt_clear = None
        
    def run(self):
        finish = False
        clock = pygame.time.Clock()
        while not finish:
            self.window.fill(Color.white)
            
            tab = pygame.draw.rect(self.window, Color.grey, (0, 0, 390, 1920))
            left_line = pygame.draw.rect(self.window, Color.grey, (0, 980, 1920, 1920))
            highlight = pygame.draw.rect(self.window, Color.black, (10, 50, 340, 5))
            right_line = pygame.draw.rect(self.window, Color.grey, (1720, 700, 200, 1000))
            
            self.bt_green  = pygame.draw.rect(self.window, Color.green, (1720, 100, 100, 100))
            self.bt_black  = pygame.draw.rect(self.window, Color.black, (1720, 200, 100, 100))
            self.bt_pink   = pygame.draw.rect(self.window, Color.pink, (1720, 300, 100, 100))
            self.bt_blue   = pygame.draw.rect(self.window, Color.blue, (1720, 400, 100, 100))
            self.bt_orange = pygame.draw.rect(self.window, Color.orange, (1720, 500, 100, 100))
            
            self.bt_red    = pygame.draw.rect(self.window, Color.red, (1820, 100, 100, 100))
            self.bt_white  = pygame.draw.rect(self.window, Color.white, (1820, 200, 100, 100))
            self.bt_brown  = pygame.draw.rect(self.window, Color.brown, (1820, 300, 100, 100))
            self.bt_yellow = pygame.draw.rect(self.window, Color.yellow, (1820, 400, 100, 100))
            self.bt_purple = pygame.draw.rect(self.window, Color.purple, (1820, 500, 100, 100))
        
            #self.window.blit(self.eraser_image, (1830, 220))
            
            self.bt_largerBrush = pygame.draw.circle(self.window, Color.black, (1870, 650), 35)
            self.bt_smallerBrush = pygame.draw.circle(self.window, Color.black, (1770, 650), 15) 
            
            for event in pygame.event.get() :
                if event.type == pygame.QUIT:
                    finish = True # Quit program
                else:
                    continue
            clock.tick(10)
            pygame.display.update()
            
if __name__ == "__main__":
    a = Test()
    a.run()
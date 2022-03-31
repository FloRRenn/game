import pygame
from pygame.locals import *
import ctypes
import ipaddress, server
from random import randint, random
from button import TextButton
from multiprocessing import Pipe, Process
from waitingMenu import PreGame as Game

bgColor = (118, 188, 194)

"""
red = (255, 0, 0)
green = (0, 255, 0)
yellow = (255, 215, 0)
white = (255, 255, 255)
black = (0, 0, 0)
blue = (38, 188, 254)
rose = (238, 130, 238)
brown = (88, 41, 0)
grey = (192, 192, 192)
"""

class Home:
    idFrame = idFrame2 = 0
    homeMenu = True
    hostMenu = joinMenu = launchGame = False
    bar = '|'
    
    def __init__(self):
        ctypes.windll.user32.SetProcessDPIAware()
        self.width = ctypes.windll.user32.GetSystemMetrics(0)
        self.height = ctypes.windll.user32.GetSystemMetrics(1)
        self.window = pygame.display.set_mode((self.width, self.height))#, pygame.FULLSCREEN)
        
        self.large_font = pygame.font.Font("font/dilo.ttf", 80)
        self.small_font = pygame.font.Font("font/dilo.ttf", 40)
        
        self.logo1 = pygame.image.load("img/lobby/logo1.png")
        self.logo2 = pygame.image.load("img/lobby/logo2.png")
        self.sun = pygame.image.load("img/lobby/soleil.png")
        self.close_image = pygame.image.load("img/lobby/croix.png")
        self.cloud = pygame.image.load("img/lobby/nuage.png")
        
        self.cloud1_X = randint(-600, 1500)
        self.cloud1_G = random() / 3 + .15
        self.cloud1_Y = randint(0, 250)
        
        self.cloud2_X = randint(400, 2000)
        self.cloud2_G = -(random() / 3 + .15)
        self.cloud2_Y = randint(0, 250)
        
        self.Host_button = TextButton('Host a party', (0, 0, 0), (int(self.width / 2), 510), self.large_font)
        self.Join_button = TextButton('Join a party', (0, 0, 0), (int(self.width / 2), 680), self.large_font)
        self.IP_button = self.LAN_button = None
        
        self.joinWithIP = self.joinWithLAN = False
        self.IpMenu = True
        self.finish = False
        
        self.procDiffu = Process()
        self.procServer = Process()
        
        self.ip = '0.0.0.0'
        self.name = ''
        
        # Song in home
        pygame.mixer.music.load("music/home.mp3")
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.1)
        
    def checkIP(self, IP : str):
        try:          
            res = ipaddress.ip_address(IP)
            return True
        
        except:
            return False
     
    def draw(self, pos):
        self.window.fill(bgColor)
        self.window.blit(self.logo1, self.logo1.get_rect(center=(int(self.width / 2), 100)))
        self.window.blit(self.sun, (1645, 22))
        self.window.blit(self.close_image, self.close_image.get_rect(topright=(self.width - 15, 15)))
        
        self.cloud1_X += self.cloud1_G
        if self.cloud1_X > 1930:
            self.cloud1_X = randint(-600, -300)
        self.window.blit(self.cloud, (int(self.cloud1_X), self.cloud1_Y))

        self.cloud2_X += self.cloud2_G
        if self.cloud2_X < -200:  
            self.cloud2_X = randint(1930, 2100)  
        self.window.blit(self.cloud, (int(self.cloud2_X), self.cloud2_Y))
    
        self.idFrame = (self.idFrame + 1) % 40 
        if self.idFrame < 20:
            self.window.blit(self.logo1, self.logo1.get_rect(center=(int(self.width / 2), 100)))
        else:
            self.window.blit(self.logo2, self.logo2.get_rect(center=(int(self.width / 2), 100)))
        
        if self.homeMenu:
            self.Host_button.draw(self.window, pos)
            self.Join_button.draw(self.window, pos)
            
        elif self.hostMenu:
            display = self.large_font.render('Enter your nickname : ' + self.name + self.bar, True, (0, 0, 0))
            self.window.blit(display, (200, 530))
            
        elif self.joinMenu:    
            if self.joinWithIP:
                if self.IpMenu:
                    textIP = self.large_font.render("Enter the IP address of the server : " + self.ip + self.bar, True, (0, 0, 0))
                    self.window.blit(textIP, (200, 530))
                
                else:
                    display = self.large_font.render('Enter your nickname : ' + self.name + self.bar, True, (0, 0, 0))
                    self.window.blit(display, (200, 530))
                    
            elif self.joinWithLAN:
                display = self.large_font.render('Enter your nickname : ' + self.name + self.bar, True, (0, 0, 0))
                self.window.blit(display, (200, 530))
                
            else:
                self.IP_button = TextButton('Join with IP', (0, 0, 0), (int(self.width / 2), 410), self.large_font)
                self.IP_button.draw(self.window, pos)
                
                self.LAN_button = TextButton('Join with LAN', (0, 0, 0), (int(self.width / 2), 610), self.large_font)
                self.LAN_button.draw(self.window, pos)
            
        pygame.display.update()

    def getEvent(self, pos):
        for event in pygame.event.get() :
            if event.type == pygame.QUIT or (event.type == MOUSEBUTTONDOWN and self.close_image.get_rect(topright = (self.width - 15, 15)).collidepoint(pos)):
                self.finish = True # Quit program
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: # pressed ENTER
                    if self.hostMenu:
                        self.ip = '127.0.0.1'
                        self.host = True
                        # Establish self-hosted server
                        self.procDiffu = Process(target = server.connectionAgain)
                        self.procDiffu.daemon = True
                        self.procDiffu.start()
                        
                        self.procServer = Process(target = server.server)
                        self.procServer.start()
                        self.launchGame = True
                        
                        print('entered to Host ')
                        
                    elif self.joinWithIP:
                        if self.name != '' and not self.IpMenu:
                            print('entered to Game (IP -> Game)')
                            self.launchGame = True
                            
                        elif self.IpMenu and self.checkIP(self.ip):
                            self.IpMenu = False
                        
                    elif self.joinWithLAN and self.name.strip() != '':
                        print('entered to Game (LAN -> Game) ')
                        self.launchGame = True
                        
                else:
                    if self.hostMenu or self.joinWithLAN or not self.IpMenu:
                        if event.key == pygame.K_BACKSPACE:
                            self.name = self.name[:-1]
                            
                        elif len(self.name) < 16:
                            self.name += event.unicode 
                            
                    elif self.joinMenu and self.IpMenu:
                        if event.key == pygame.K_BACKSPACE:
                            self.ip = self.ip[:-1]
                            
                        elif len(self.ip) < 16:
                            self.ip += event.unicode
                        
            elif event.type == MOUSEBUTTONDOWN and event.button == 1: # Clicked
                if self.homeMenu:
                    if self.Host_button.border_position.collidepoint(pos):
                        self.homeMenu = False
                        self.hostMenu = True
                        
                    elif self.Join_button.border_position.collidepoint(pos):
                        self.homeMenu = False
                        self.joinMenu = True
                        
                else:
                    if self.IP_button.border_position.collidepoint(pos):
                        self.joinWithIP = True
                        
                    elif self.LAN_button.border_position.collidepoint(pos):
                        self.joinWithLAN = True
    
    def run(self):
        clock = pygame.time.Clock()
        while not self.finish:
            clock.tick(80)
            pos = pygame.mouse.get_pos()
            self.draw(pos)
            self.getEvent(pos)     
            
            if self.launchGame:
                g = Game(self.name, self.ip.strip(), self.procDiffu, 
                         self.window, self.width, self.height)

                self.finish = g.run()
                
        pygame.quit()
        if self.procServer.is_alive():
            self.procServer.terminate()
            self.procServer.join()
            
if __name__ == '__main__':
    pygame.font.init()
    pygame.init()
    
    g = Home()
    g.run() 
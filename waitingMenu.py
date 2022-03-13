import pygame
import client
from random import choice
from pygame.locals import *
from multiprocessing import Process, Pipe
from drawingPlayer import DrawingPlayer
from guessingPlayer import GuessingPlayer
import pymongo, os

username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")
databaseName = os.environ.get("DATABASE")

class Window:
    dot = ' . '
    
    def __init__(self, window, width, height, ):
        self.window = window
        self.width = width
        self.height = height
        
        self.large_font = pygame.font.SysFont("roboto-bold", 65)
        self.count = 0
        
        self.play = pygame.image.load("img/lobby/play.png")
        self.play_pos = self.play.get_rect(topright = (self.width - 15, 15))
        
    def dotAppear(self):
        if self.count < 5:
            self.count += 1
        else:
            self.count = 0
        return self.count
        
    def draw(self, players, host : bool):
        if host:
            self.window.fill((255, 255, 255))
            texteConn = self.large_font.render(str(len(players)) + ' people are connected', True, (0, 0, 0))
            self.window.blit(texteConn, (0, 0))
            
            self.window.blit(self.play, self.play_pos)
            
            yMsg = 60
            for player in players: 
                display = self.large_font.render(players[player] + ' is connected', True, (0, 0, 0))
                self.window.blit(display, (60, yMsg))
                yMsg += 60
            
        else:
            self.window.fill((255, 255, 255))
            texteConn = self.large_font.render('Waiting for begin' + self.dot * self.dotAppear(), True, (0, 0, 0))
            self.window.blit(texteConn, (0, 0))
            
        pygame.display.flip()
        
    def next(self):
        self.window.fill((255, 255, 255))
        texteConn = self.large_font.render('Enter' + self.dot * self.dotAppear(), True, (0, 0, 0))
        self.window.blit(texteConn, (0, 0))
        pygame.display.flip()
        
    
class PreGame(Window):
    def __init__(self, name, ip, procDiffu, window, width, height):
        super().__init__(window, width, height)
        self.name = name
        self.ip = ip
        self.procDiffu = procDiffu
        
        self.players = {}
        self.scores = {}
        self.roles = {}
        self.idPlayer = 0
        self.IDnumber = None
        self.state = None
        self.launchGame = False
        self.roundNumber = 0
        self.maxRound = 0
        self.roleDrawing = -1

        self.tunnelParent, self.tunnelChild = Pipe()
        self.procClient = Process(target = client.client, args=(ip, self.tunnelChild, name))
        self.procClient.start()
        
        if self.ip == "127.0.0.1":
            cluster = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@cluster0.y5mnt.mongodb.net/{databaseName}?retryWrites=true&w=majority")
            self.db = cluster.insta 
             
            self.host = True
            
        else:
            self.host = False
        
    def receiveData(self):
        if self.tunnelParent.poll():
            abc = self.tunnelParent.recv()
            data = abc.decode().split(",")
            
            if self.host:
                if data[0] == 'P':  
                    self.players[self.idPlayer] = data[1]
                    
                    if data[1] == self.name:
                        self.IDnumber = self.idPlayer
                    self.idPlayer += 1
                    
                elif data[0] == 'F': # Disconnect
                    return False
                
            else:
                if data[0].startswith('T'):  # Decode the info from the Players
                    self.maxRound = int(data[0].replace('T', ''))
                    
                    data = data[1:]  # Remove 'T'
                    for player in data:
                        infos = player.split(";")  # 0;Marcel;L
                        
                        self.players[int(infos[0])] = infos[1]
                        self.roles[int(infos[0])] = infos[2]
                        self.scores[int(infos[0])] = 0
                        
                        if infos[1] == self.name:
                            self.IDnumber = infos[0]
                            self.state = infos[2]
                    
                    self.launchGame = True
                    
                elif data[0] == 'F': # Disconnect
                    return False
        return True
    
    def getNewRound(self):
        temp = self.roundNumber    
        
        while self.roundNumber == temp:
            data = self.db['game'].find({})
            
            for i in data:
                if i['round'] != self.roundNumber:
                    self.roundNumber = i['round']
                    self.roleDrawing = i['draw']
    
    def getHostEvent(self, event, pos):
        if event.type == MOUSEBUTTONDOWN and self.play_pos.collidepoint(pos):
            if len(self.players) >= 2:
                if self.procDiffu.is_alive():
                    self.procDiffu.terminate()
                    self.procDiffu.join()
                
                self.maxRound = len(self.players)   
                
                playerTable = f"T{self.maxRound}"
                idD = list(self.players.keys())[0]
                
                if idD == self.IDnumber:
                    self.state = 'D'
                else:
                    self.state = 'L'
                    
                for playerID in self.players:  # Sending all names + roles
                    self.scores[playerID] = 0
                    playerTable = playerTable + "," + str(playerID) + ";" + self.players[playerID] + ";"
                    
                    if playerID == idD:
                        self.roles[playerID] = 'D'
                        playerTable += 'D'
                        
                    else:
                        self.roles[playerID] = 'L'
                        playerTable += 'L'
                
                # "T,0;Michel;L,1;Marcel;D,2;Jean;L,3" == T,id;name;role
                self.tunnelParent.send(playerTable.encode())
                
                #LAUNCH GAME
                self.launchGame = True
                
    def clearWindow(self):
        self.window.fill((255, 255, 255))
        pygame.display.flip()
        
    def updateRole(self):
        """
        Role: 
            D == Drawing
            L == Guessing
        """
        
        for key, value in self.roles.items():
            if key == self.roleDrawing:
                self.roles[key] = 'D'
            else:
                self.roles[key] = 'L'
    
    def run(self):
        isConnected = True
        clock = pygame.time.Clock()
        
        while isConnected:
            isConnected = self.receiveData()
            
            if isConnected:
                self.draw(self.players, self.host)
                pos = pygame.mouse.get_pos()
                
                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE): # Quit Game
                        self.tunnelParent.send('F'.encode())
                        isConnected = False
                    
                    elif self.host:
                        self.getHostEvent(event, pos)
                        
                        
            if self.launchGame:
                self.clearWindow()
                print('==> LAUNCH GAME')
                break
                    
            clock.tick(5)
        
        if isConnected == False:
            return True

        while self.roundNumber < self.maxRound * 2:
            if self.host:
                self.roundNumber += 1
                self.roleDrawing += 1
                if self.roleDrawing > self.maxRound - 1:
                    self.roleDrawing = 0
                
                self.db['game'].update_one({'round' : self.roundNumber - 1}, {'$set' : {'round' : self.roundNumber, 'draw' : self.roleDrawing}})
                
                mess = f'Y,{self.roundNumber}'
                self.tunnelParent.send(mess.encode())
            
            else:            
                self.getNewRound()
            
            self.updateRole()
            #print(self.roles, self.IDnumber)
            if self.roles[int(self.IDnumber)] == 'D':
                game = DrawingPlayer(self.roundNumber, self.IDnumber, self.tunnelParent,
                                self.players, self.scores, self.roles,
                                self.window, self.width, self.height)
            
            else:
                game = GuessingPlayer(self.roundNumber, self.IDnumber, self.tunnelParent,
                                    self.players, self.scores, self.roles,
                                    self.window, self.width, self.height)
                
            self.players, self.scores, self.roles, self.roundNumber = game.run()

        pygame.quit()
        if self.procClient.is_alive():
            self.procClient.join()
            
        return True
        
        

            
            
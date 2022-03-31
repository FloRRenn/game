import pygame, time
import client
from random import choice
from pygame.locals import *
from multiprocessing import Process, Pipe
from drawingPlayer import DrawingPlayer
from guessingPlayer import GuessingPlayer

class Window:
    dot = ' . '
    
    def __init__(self, window, width, height, ):
        self.window = window
        self.width = width
        self.height = height
        
        self.large_font = pygame.font.Font("font/dilo.ttf", 65)
        self.count = 0
        
        self.play = pygame.image.load("img/lobby/play.png")
        self.play_pos = self.play.get_rect(topright = (self.width - 15, 15))
        
        self.notEnoughSound = pygame.mixer.Sound("music/notEnough.wav")
        self.roundBeginSound = pygame.mixer.Sound("music/newRound.wav")
        
        
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
                
            else:
                self.notEnoughSound.play()
                
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
                
    def updateDataNextRound(self):
        self.roleDrawing += 1
        if self.roleDrawing > self.maxRound - 1:
            self.roleDrawing = 0
        self.roundNumber += 1
        
        data = f'I,{self.roleDrawing},{self.roundNumber}'
        self.tunnelParent.send(data.encode())
        
        clientRecieved = 0
        while clientRecieved != len(self.players) - 1:
            if self.tunnelParent.poll():
                abc = self.tunnelParent.recv()
                data = abc.decode().split(",")
                
                if data[0] == 'ok':
                    clientRecieved += 1
                    
    def getDataNextRound(self):
        temp = self.roundNumber
        
        while temp == self.roundNumber:
            if self.tunnelParent.poll():
                abc = self.tunnelParent.recv()
                data = abc.decode().split(",")
                
                if data[0] == 'I':
                    self.roleDrawing = int(data[1])
                    self.roundNumber = int(data[2])
                    self.tunnelParent.send('ok,'.encode())
                
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
        
        pygame.mixer.music.stop()
        if isConnected == False:
            return True   
        
        while self.roundNumber < self.maxRound:
            if self.host:
                self.updateDataNextRound()

            else:           
                self.getDataNextRound() 
            
            self.updateRole()
            self.roundBeginSound.play()
            
            if self.roles[int(self.IDnumber)] == 'D':
                game = DrawingPlayer(self.roundNumber, self.IDnumber, self.tunnelParent,
                                self.players, self.scores, self.roles,
                                self.window, self.width, self.height)
            
            else:
                game = GuessingPlayer(self.roundNumber, self.IDnumber, self.tunnelParent,
                                    self.players, self.scores, self.roles,
                                    self.window, self.width, self.height)
                
            self.players, self.scores, self.roles, self.roundNumber = game.run()
            print(self.players, self.scores)
            
        scoreBoard = {}
        for i in range(len(self.players)):
            scoreBoard[self.players[i]] = self.scores[i]
        scoreBoard = {player: score for player, score in sorted(scoreBoard.items(), key = lambda item: item[1], reverse = True)} # Decreasing order by score
        endTime = time.time() + 30
        
        print(scoreBoard, endTime)
        self.clearWindow()
        while True:
            timer = endTime - time.time()
            if timer < 0:
                break
            
            yMsg = 100
            top = 1
            for player, score in scoreBoard.items(): 
                display = self.large_font.render(f'Top {top}. {player} : {score}', True, (0, 0, 0))
                self.window.blit(display, (300, yMsg))
                yMsg += 60
                top += 1
                
            for event in pygame.event.get():
                continue
            
            pygame.display.flip()

        pygame.quit()
        if self.procClient.is_alive():
            self.procClient.join()
            
        return True
        
        

            
            
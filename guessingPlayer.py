import pygame
from color import Color
from time import time

class Window(object):
    def __init__(self, window, width, height):
        self.window = window
        self.width = width
        self.height = height
        
        self.small_font = pygame.font.Font("font/Ingame.otf", 35)
        self.large_font = pygame.font.Font("font/dilo.ttf", 50)
        
        self.brush = pygame.image.load("img/pinceau.png").convert()
        self.submitSound = pygame.mixer.Sound("music/submit.ogg")
        
    def drawBoard(self, display_word, round_number):
        bgColor_palette = pygame.draw.rect(self.window, Color.white, (1720, 100, 200, 980))
        tab = pygame.draw.rect(self.window, Color.grey, (0, 0, 390, 1920))
        line1 = pygame.draw.rect(self.window, Color.black, (390, 0, 10, 980))
        line2 = pygame.draw.rect(self.window, Color.black, (0, 970, 1920, 10))
        left_line = pygame.draw.rect(self.window, Color.grey, (0, 980, 1920, 1920))
        highlight = pygame.draw.rect(self.window, Color.black, (10, 50, 340, 5))
        line12 = pygame.draw.rect(self.window, Color.black, (390, 100, 1920, 5))
        effac = pygame.draw.rect(self.window, Color.grey, (1720, 10, 190, 80))
        
        round_number = self.large_font.render(f'Round {round_number}', True, (0, 0, 0))
        self.window.blit(round_number, (1300, 40))  
        self.window.blit(display_word, (1400, 1000))
    
    def timerDisplay(self, time):
        if time < 0:
            time = 0
            
        timer_display = self.large_font.render(str(time), True, (0, 0, 0))
        self.window.blit(timer_display, (1810, 610))
            
    def playersDisplay(self, players, scores, roles):
        onlinePlater_display = self.large_font.render('Online players : ', True, (0, 0, 0))  # txt,antialiasing,coul
        self.window.blit(onlinePlater_display, (10, 0))

        pos_txtPlayer = 0
        for player in players:
            playerName_display = self.large_font.render(players[player] + " : " + str(scores[player]), True, (0, 0, 0))
            self.window.blit(playerName_display, (10, 60 + pos_txtPlayer * 50))
            
            if roles[player] == "D":
                self.window.blit(self.brush, (340, 60 + pos_txtPlayer * 50))
                
            pos_txtPlayer += 1
            
    def chatDisplay(self, list_msg_chat):
        for i in range(10):
            list_msg_chat = list_msg_chat[-10:]
            textchat = self.small_font.render(list_msg_chat[i], True, (0, 0, 0))
            self.window.blit(textchat, (50, 480 + 50 * i))
            
    def updateChatting(self, chat):
        txt_WrittenWord = self.large_font.render('Write your word : ' + chat, True,(0, 0, 0))
        self.window.blit(txt_WrittenWord, (50, 1000))

class GuessingPlayer(Window):
    roundTime = 60
    checkShowHint = {
        41 : True,
        21 : True,
        11 : True,
        9 : True,
    }
    
    def __init__(self, roundNumber, IDnumber, tunnelParent, players, scores, roles, window, width, height):
        super().__init__(window, width, height)
        self.tunnelParent = tunnelParent
        
        self.roundNumber = roundNumber
        self.IDnumber = IDnumber
    
        self.players = players
        self.scores = scores
        self.roles = roles
        
        self.list_msg_chat = [' '] * 10
        
        self.writingWord = ''
        self.guessedWord = 'Word is not chosen'
        self.displayGuessedWord = 'Word is not chosen'
        self.displayWord = None
        self.wordHint = -1
        self.cache_word = None
        
        self.finishTime = 0
        self.isFound = False
        
    def analyzeData(self):
        if self.tunnelParent.poll():
            for raw_data in self.tunnelParent.recv().decode().split("@"):
                data = raw_data.split(",")
                print(data)
                # Break program
                if data[0] == "Q":
                    return True
                
                # All players found the word
                elif data[0] == 'K':
                    self.finishTime = time()
                
                # Data is about drawing
                elif data[0] == 'D' and self.guessedWord != 'Word is not chosen':
                    pos = data[1].split(";")
                    pos = tuple(map(int, pos))
                    
                    last = data[2].split(";")
                    last = tuple(map(int, last))
                    
                    color = data[3].split(";")
                    color = tuple(map(int, color))
                    
                    radius = int(data[4])
                    
                    pygame.display.update(pygame.draw.circle(self.window, color, pos, radius))
                    self.design(color, pos, last, radius)

                # Player left   
                elif data[0] == 'F':
                    del self.players[int(data[1])]
                    del self.roles[int(data[1])]

                # Get players's chat
                elif data[0] == 't':
                    self.list_msg_chat.append(self.players[int(data[1])] + " : " + data[2])

                # Clear board
                elif data[0] == "E":
                    pygame.draw.rect(self.window, Color.white, (400, 105, 1320, 865))

                # Get guessed word
                elif data[0] == "M":
                    self.guessedWord= data[1]
                    self.finishTime = int(time() + self.roundTime)
                    self.showWord()

                # Si un joueur a trouvé le mot
                elif data[0] == "O":
                    self.list_msg_chat.append(self.players[int(data[1])] + " found the word")

                # Time out or all players guessed the word
                elif data[0] == "R":
                    self.list_msg_chat.append("This is " + self.guessedWord)

                elif data[0] == "P":
                    self.scores[int(data[1])] += int(data[2])
                    
        return False
    
    def showWord(self, position : int = None):
        if position is None:
            self.cache_word = ['_'] * len(self.guessedWord)
            
        else:
            self.cache_word[position] = self.guessedWord[position]
            
        self.displayGuessedWord = str(' '.join(self.cache_word))
        
    def showHint(self, timer):
        if timer in [41, 21, 11, 9]:
            if not self.checkShowHint[timer]:
                if timer == 41:
                    pygame.mixer.music.load("music/40sec.mp3")
                
                elif timer == 21:
                    pygame.mixer.music.load("music/20sec.mp3")
                
                elif timer == 11:
                    pygame.mixer.music.load("music/10sec.mp3")
                    
                elif timer == 9:
                    pygame.mixer.music.load("music/ticktack.wav")
                    
                pygame.mixer.music.play(loops=0)
                return
            self.checkShowHint[timer] = False
            
            self.wordHint += 1
            self.showWord(self.wordHint)
                    
    def design(self, color, pos, last, radius):
        dx = last[0] - pos[0]  # Calculate the distance between the two positions
        dy = last[1] - pos[1]
        distance = max(abs(dx), abs(dy))
        
        for i in range(distance):
            x = int(pos[0] + float(i) / distance * dx) 
            y = int(pos[1] + float(i) / distance * dy)
            
            # Update the window with a new circle
            pygame.display.update(pygame.draw.circle(self.window, color, (x, y), radius))
            
    def getEvents(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and self.writingWord != '':
                if self.writingWord == self.guessedWord:
                    self.displayWord = self.large_font.render(self.guessedWord, True, (0, 0, 0))
                    self.isFound = True
                    
                    point = int(self.finishTime - time())
                    self.scores[int(self.IDnumber)] += point
                    self.list_msg_chat.append("You found the word")
                    
                    # Let others know you found the word
                    self.tunnelParent.send(("O," + str(self.IDnumber) + '@').encode())
                    self.tunnelParent.send(("P," + str(self.IDnumber) + "," + str(point) + '@').encode())

                else:
                    # Update chat
                    self.list_msg_chat.append(self.players[int(self.IDnumber)] + " : " + self.writingWord)
                    self.tunnelParent.send(("t," + str(self.IDnumber) + "," + self.writingWord + '@').encode())
                
                self.submitSound.play(0, 0, 0)
                self.writingWord = '' 

            # Word, not a sentence
            elif event.key == pygame.K_BACKSPACE:
                self.writingWord = self.writingWord[:-1]

            # Update chatting
            elif len(self.writingWord) < 16 and self.guessedWord != "Word is not chosen":
                self.writingWord += event.unicode

    def run(self):
        isRunning = True
        
        clock = pygame.time.Clock()
        while isRunning:
            close = self.analyzeData()
            if close or len(self.players) <= 1:
                break
            
            if self.isFound == False:
                self.displayWord = self.large_font.render(self.displayGuessedWord, True, (0, 0, 0))
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.tunnelParent.send(("F," + str(self.IDnumber) + '@').encode())
                    return None,None,None,None
                
                else:
                    self.getEvents(event)
                    
            entete = pygame.draw.rect(self.window, Color.grey, (400, 0, 1920, 100))  
            self.drawBoard(self.displayWord, self.roundNumber)
            
            timeleft = self.finishTime - time()
            self.timerDisplay(timeleft)
            self.showHint(int(timeleft))
            
            self.playersDisplay(self.players, self.scores, self.roles)
            self.chatDisplay(self.list_msg_chat)
            self.updateChatting(self.writingWord)
            
            pygame.display.flip()        
            clock.tick(50)
            
        return self.players, self.scores, self.roles, self.roundNumber
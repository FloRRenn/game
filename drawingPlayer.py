import pygame
from color import Color
from random import choice
from button import TextButton
from time import time

class Window(object):
    def __init__(self, window, width, height):
        self.window = window
        self.width = width
        self.height = height
        
        self.bt_red = self.bt_yellow = self.bt_green = self.bt_blue = self.bt_orange = None
        self.bt_pink = self.bt_brown = self.bt_black = self.bt_white = self.bt_purple = None
        self.bt_largerBrush = self.bt_smallerBrush = self.bt_clear = None
        
        self.eraser_image = pygame.image.load("img/gomme1.png").convert_alpha()
        self.image = pygame.image.load("img/ima.png").convert_alpha()
        self.circle_1 = pygame.image.load("img/pal1.png").convert_alpha()
        self.circle_2 = pygame.image.load("img/pal2.png").convert_alpha()
        self.brush = pygame.image.load("img/pinceau.png").convert()
        
        self.small_font = pygame.font.Font("font/Ingame.otf", 35)
        self.large_font = pygame.font.Font("font/dilo.ttf", 50)
        
    def drawButton(self):
        pygame.draw.rect(self.window, Color.white, (1820, 500, 100, 200))
        pygame.draw.rect(self.window, Color.white, (1720, 500, 100, 200))
        
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
    
        self.window.blit(self.eraser_image, (1830, 220))
        
        self.bt_largerBrush = pygame.draw.circle(self.window, Color.black, (1870, 650), 35)
        self.bt_smallerBrush = pygame.draw.circle(self.window, Color.black, (1770, 650), 15) 
        
    def drawBoard(self, roundNumber):
        entete = pygame.draw.rect(self.window, Color.grey, (400, 0, 1920, 100))
        tab = pygame.draw.rect(self.window, Color.grey, (0, 0, 390, 1920))
        underline = pygame.draw.rect(self.window, Color.black, (10, 60, 340, 5))
        left_line = pygame.draw.rect(self.window, Color.grey, (0, 980, 1920, 1920))
        right_line = pygame.draw.rect(self.window, Color.grey, (1720, 700, 200, 1000))
        
        line1 = pygame.draw.rect(self.window, Color.black, (390, 0, 10, 980))
        line12 = pygame.draw.rect(self.window, Color.black, (390, 100, 1920, 5))
        line2 = pygame.draw.rect(self.window, Color.black, (0, 970, 1920, 10))
        line9 = pygame.draw.rect(self.window, Color.black, (1720, 100, 10, 1000))
        line10 = pygame.draw.rect(self.window, Color.black, (1820, 100, 5, 500))
        
        
        """
        line4 = pygame.draw.rect(self.window, Color.black, (1720, 200, 1000, 5))
        
        
        line6 = pygame.draw.rect(self.window, Color.black, (1720, 400, 1000, 5))
        line7 = pygame.draw.rect(self.window, Color.black, (1720, 500, 1000, 5))
        line8 = pygame.draw.rect(self.window, Color.black, (1720, 600, 1000, 5))
        line9 = pygame.draw.rect(self.window, Color.black, (1720, 100, 10, 1000))
        line10 = pygame.draw.rect(self.window, Color.black, (1820, 100, 5, 500))
        line11 = pygame.draw.rect(self.window, Color.black, (1915, 100, 5, 500))
        """
        
        round_number = self.large_font.render(f'Round {roundNumber}', True, (0, 0, 0))
        self.window.blit(round_number, (1300, 40))  
        
        self.bt_clear = pygame.draw.rect(self.window, Color.white, (1700, 10, 200, 80))
        clearText = self.small_font.render("Clear a Board", True, (0, 0, 0))
        self.window.blit(clearText, (1703, 35))    
        
    def infoDisplay(self, radius, color_text, color):
        radius_diplay = self.large_font.render('radius : ' + str(radius), True, (0, 0, 0))
        self.window.blit(radius_diplay, (600, 1000))
        
        color_display = self.large_font.render(color_text, True, color)
        self.window.blit(color_display, (900, 1000))
        
    def drawAll(self, radius, color_text, color, round_number):
        self.drawButton()
        self.drawBoard(round_number)
        self.infoDisplay(radius, color_text, color)
        
    def timerDisplay(self, time):
        if time < 0:
            time = 0
        timer_display = self.large_font.render(str(time), True, (0, 0, 0))
        self.window.blit(timer_display, (1810, 800))

class DrawingPlayer(Window):
    roundTime = 60
    
    def __init__(self, roundNumber, IDnumber, tunnelParent, players, scores, roles, window, width, height):
        super().__init__(window, width, height)
        
        self.roundNumber = roundNumber
        self.tunnelParent = tunnelParent
        
        self.IDnumber = IDnumber
        self.players = players
        self.scores = scores
        self.roles = roles
        
        self.list_msg_chat = [' '] * 10
        self.list_guessedWords = [word.strip() for word in open("words.txt", encoding = "utf-8")]
        
        self.found = self.idFrame = 0
        self.radius = 10
        self.color = Color.black
        self.colorText = 'Black'
        
        self.guessedWord = 'Word is not chosen'
        self.is_selection_word = True
        self.isPressing = False
        self.showCase = self.allFound = True
        
        self.finish_time = 0
    
    def analyzeData(self):
        if self.tunnelParent.poll():
            for raw_data in self.tunnelParent.recv().decode().split("@"):
                data = raw_data.split(",")
                
                # If a player has left
                if data[0] == 'F':
                    self.list_msg_chat.append(self.players[int(data[1])] + " has left the match.")
                    del self.players[int(data[1])]
                    del self.roles[int(data[1])]
                
                # # If a player sent a message
                elif data[0] == 't':
                    # Add nickname and his text to list chat
                    self.list_msg_chat.append(self.players[int(data[1])] + " : " + data[2])
                    
                # If a player found the word
                elif data[0] == "O":
                    self.list_msg_chat.append(self.players[int(data[1])] + " found the word!!!")
                    self.found += 1
                    #player_guessed_song.play(0, 0, 0)
                   
                # Update player's point 
                elif data[0] == "P":
                    print(data)
                    self.scores[int(data[1])] += int(data[2])
                    
                # If a player has activated HINT
                elif data[0] == "V":
                    self.hint = 1
    
    def design(self, color, pos, last, radius):
        dx = last[0] - pos[0]  # Calculate the distance between the two positions
        dy = last[1] - pos[1]
        distance = max(abs(dx), abs(dy))
        
        for i in range(distance):
            x = int(pos[0] + float(i) / distance * dx) 
            y = int(pos[1] + float(i) / distance * dy)
            
            # Update the window with a new circle
            pygame.display.update(pygame.draw.circle(self.window, color, (x, y), radius))
    
    def getEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.guessedWord != 'Word is not chosen':
            pygame.draw.circle(self.window, self.color, event.pos, self.radius) #Make a circle at the clicking position
            self.isPressing = True

        # If you get the mouse button
        elif event.type == pygame.MOUSEBUTTONUP:
            self.isPressing = False

        # If the mouse moves and the clique is pressed
        elif event.type == pygame.MOUSEMOTION:
            if self.isPressing:
                # Update the window with a new circle right next to the old
                pygame.display.update(pygame.draw.circle(self.window, self.color, event.pos, self.radius))
                self.design(self.color, event.pos, self.lastpos, self.radius)
                
                # Send info to the server about positions and color of new circle
                # D,posX;posY,lastposX;lastposY,R;G;B,radius@
                self.tunnelParent.send(('D,' + str(event.pos[0]) + ";" + str(event.pos[1]) + "," + str(
                    self.lastpos[0]) + ";" + str(self.lastpos[1]) + "," + str(self.color[0]) + ";" + str(
                    self.color[1]) + ";" + str(self.color[2]) + "," + str(self.radius) + '@').encode())
                
            self.lastpos = event.pos
            
    def chooseWord(self, pos):
        if self.is_selection_word:
            self.word_1 = choice(self.list_guessedWords)
            self.word_2 = choice(self.list_guessedWords)
            self.word_3 = choice(self.list_guessedWords)
            
            self.is_selection_word = False
            self.clear()
            
        bt_Word1 = TextButton(self.word_1, Color.black, (int(self.width / 2), 410), self.large_font)
        bt_Word2 = TextButton(self.word_2, Color.black, (int(self.width / 2), 510), self.large_font)
        bt_Word3 = TextButton(self.word_3, Color.black, (int(self.width / 2), 610), self.large_font)
        
        if bt_Word1.draw(self.window, pos) and pygame.mouse.get_pressed() == (1, 0, 0):
            self.guessedWord = self.word_1
            
        elif bt_Word2.draw(self.window, pos) and pygame.mouse.get_pressed() == (1, 0, 0):
            self.guessedWord = self.word_2
            
        elif bt_Word3.draw(self.window, pos) and pygame.mouse.get_pressed() == (1, 0, 0):
            self.guessedWord = self.word_3
            
        if self.guessedWord != 'Word is not chosen':
            self.tunnelParent.send(("M" + "," + self.guessedWord + '@').encode())  # Send guessed word to other players
            pygame.draw.rect(self.window, Color.white, (400, 105, 1320, 865))  # Erase the window
            self.finish_time = time() + self.roundTime
            
    def clear(self):
        self.tunnelParent.send("E".encode())
        
        self.color = Color.black
        self.radius = 10
        pygame.draw.rect(self.window, Color.white, (400, 105, 1320, 865))
        
    def clearBoard(self):
        pygame.draw.rect(self.window, Color.black, (1700, 10, 200, 5))
        pygame.draw.rect(self.window, Color.black, (1700, 10, 5, 80))
        pygame.draw.rect(self.window, Color.black, (1900, 10, 5, 80))
        pygame.draw.rect(self.window, Color.black, (1700, 85, 200, 5))
        
        if pygame.mouse.get_pressed() == (1, 0, 0):
            pygame.draw.rect(self.window, Color.white, (400, 105, 1320, 865))
            self.tunnelParent.send("E".encode())
            
    def selection_circle1(self):  # + radius
        if pygame.mouse.get_pressed() == (1, 0, 0):  # Change of radius during a click
            self.radius = self.radius + 5
        pygame.time.wait(100)

    def selection_circle2(self):  # - radius
        if pygame.mouse.get_pressed() == (1, 0, 0):  # Change of radius during a click
            if self.radius > 5:
                self.radius = self.radius - 5
        pygame.time.wait(100)
            
    def selection(self, button, color, text):
        self.idFrame = (self.idFrame + 1) % 40
        
        if self.idFrame < 30:
            self.window.blit(self.circle_1, button)
        else:
            self.window.blit(self.circle_2, button)
            
        if pygame.mouse.get_pressed() == (1, 0, 0): 
            self.color = color
            self.colorText = text
            
    def colorSelections(self, pos):
        if self.bt_yellow.collidepoint(pos):
            self.selection(self.bt_yellow, Color.yellow, 'Yellow')
            
        elif self.bt_red.collidepoint(pos):
            self.selection(self.bt_red, Color.red, 'Red')
            
        elif self.bt_green.collidepoint(pos):
            self.selection(self.bt_green, Color.green, 'Green')
            
        elif self.bt_white.collidepoint(pos):
            self.selection(self.bt_white, Color.white, 'White')
            
        elif self.bt_black.collidepoint(pos):
            self.selection(self.bt_black, Color.black, 'Black')
            
        elif self.bt_brown.collidepoint(pos):
            self.selection(self.bt_brown, Color.brown, 'Brown')
            
        elif self.bt_pink.collidepoint(pos):
            self.selection(self.bt_pink, Color.pink, 'Pink')
            
        elif self.bt_blue.collidepoint(pos):
            self.selection(self.bt_blue, Color.blue, 'Blue')
            
        elif self.bt_orange.collidepoint(pos):
            self.selection(self.bt_orange, Color.orange, 'Orange')
            
        elif self.bt_purple.collidepoint(pos):
            self.selection(self.bt_purple, Color.purple, 'Purple')
            
        elif self.bt_largerBrush.collidepoint(pos):
            self.selection_circle1()
            
        elif self.bt_smallerBrush.collidepoint(pos):
            self.selection_circle2()
            
        elif self.bt_clear.collidepoint(pos):
            self.clearBoard()
            
    def showWord(self):
        guessedWord_display = self.large_font.render(self.guessedWord, True, (0, 0, 0))
        self.window.blit(guessedWord_display, (1400, 1000))
        
    def updateChat(self, list_msg_chat):
        for chat in range(10):
            list_msg_chat = list_msg_chat[-10:]
            textchat = self.small_font.render(list_msg_chat[chat], True, (0, 0, 0))
            self.window.blit(textchat, (30, 480 + 50 * chat))
            
    def playerDisplay(self):
        onlinePlater_display = self.large_font.render('Online players : ', True, (0, 0, 0))  # txt,antialiasing,coul
        self.window.blit(onlinePlater_display, (10, 0))
        pos_txtPlayer = 0
        
        for player in self.players:
            playerName_display = self.large_font.render(self.players[player] + " : " + str(self.scores[player]), True, (0, 0, 0))
            self.window.blit(playerName_display, (10, 70 + pos_txtPlayer * 50))
            
            if self.roles[player] == "D":
                self.window.blit(self.brush, (340, 60 + pos_txtPlayer * 50))
            pos_txtPlayer += 1
        
    def run(self):
        isRunning = True
        clock = pygame.time.Clock()
        
        while isRunning:
            self.analyzeData()
            pos = pygame.mouse.get_pos() 
            self.drawAll(self.radius, self.colorText, self.color, self.roundNumber)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    # Send the info if player leaves the server
                    self.tunnelParent.send(("F," + str(self.IDnumber) + '@').encode())
                    return None,None,None,None
                    
                else:
                    self.getEvent(event)
                    
            
            if self.guessedWord == 'Word is not chosen':
                self.chooseWord(pos)
                
            else:
                timeleft = int(self.finish_time - time())
                self.timerDisplay(timeleft)
                
                self.colorSelections(pos)
                self.showWord()
                self.updateChat(self.list_msg_chat)
                self.playerDisplay()
                
                if timeleft <= 0 or self.found == len(self.players) - 1:
                    pygame.draw.rect(self.window, Color.white, (400, 105, 1320, 865))
                    
                    if self.showCase:
                        self.tunnelParent.send(("R," + str(self.IDnumber) + '@').encode())
                        self.showCase = False
                        
                    if timeleft == -5:
                        self.tunnelParent.send('Q,break@'.encode())
                        break
                    
                    elif self.found == len(self.players) - 1 and self.allFound:
                        self.allFound = False
                        self.finish_time = time()
                        self.tunnelParent.send('K,@'.encode())

            pygame.display.flip()        
            clock.tick(50)
        
        return self.players, self.scores, self.roles, self.roundNumber
            
             
        
        
        
    
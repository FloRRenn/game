import pygame

class TextButton(object):
    def __init__(self, buttonName, buttonColor, position_center, font):
        self.buttonName = buttonName
        self.buttonColor = buttonColor
        self.position_center = position_center
        self.font = font
        
        self.button = None
        self.border = self.padding = self.shadow =  None
        self.button_position = self.border_position = self.padding_position = None
        
        self.createALL()
        
    def createButton(self):
        self.button = self.font.render(self.buttonName, True, self.buttonColor)
        self.button_position = self.button.get_rect(center = self.position_center)
        
    def createBoder(self):
        self.border = pygame.Surface((self.button_position[2] + 2 * 10, self.button_position[3] + 2 * 10))
        self.border.fill(self.buttonColor)
        self.border_position = self.border.get_rect(center = self.position_center)
        
    def createShadow(self):
        self.shadow = pygame.Surface((self.button_position[2] +10, self.button_position[3] + 10))
        self.shadow.set_alpha(100)
        self.shadow.fill(self.buttonColor)
        
    def createPadding(self):
        self.padding = pygame.Surface((self.button_position[2] + 10, self.button_position[3] + 10))
        self.padding.fill((118, 188, 194))
        self.padding_position = self.padding.get_rect(center = self.position_center)
        
    def createALL(self):
        self.createButton()
        self.createBoder()
        self.createShadow()
        self.createPadding()
        
    def draw(self, window, position):
        window.blit(self.border, self.border_position)
        window.blit(self.padding, self.padding_position)  
        window.blit(self.button, self.button_position)
        
        if self.border_position.collidepoint(position):
            window.blit(self.shadow, self.padding_position)
            return True
        
        return False
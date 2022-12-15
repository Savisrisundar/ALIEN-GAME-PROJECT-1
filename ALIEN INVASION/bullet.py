import pygame
from pygame.sprite import Sprite

#Sprite is a gaming term used to create multiple bullets and store it in a single entity

class Bullet(Sprite):
    def __init__(self,ai_game):
        super().__init__()
        self.screen=ai_game.screen
        self.settings=ai_game.settings
        self.color=self.settings.bullet_color
        #create a bullet at that position
        self.rect=pygame.Rect(0,0,self.settings.bullet_width,self.settings.bullet_height)
        self.rect.midtop=ai_game.ship.rect.midtop
        self.y=float(self.rect.y)

    def update(self):
        self.y -=self.settings.bullet_speed
        #update the rect position
        self.rect.y=self.y

    def draw_bullets(self):
        pygame.draw.rect(self.screen,self.color,self.rect)
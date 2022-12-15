import pygame 
from pygame.sprite import Sprite
class Ship(Sprite):
    def __init__(self,ai_game):
        super().__init__()
        self.screen=ai_game.screen
        self.settings=ai_game.settings

        self.screen_rect=ai_game.screen.get_rect()
        self.image=pygame.image.load('IMAGES/ship.bmp')
        self.rect=self.image.get_rect()
        self.rect.midbottom=self.screen_rect.midbottom
        # giving float value to change the speed in decimals
        self.x=float(self.rect.x)
        # initializing right and left
        self.moving_right = False
        self.moving_left = False
    def center_ship(self):
        self.rect.midbottom=self.screen_rect.midbottom
        self.x=float(self.rect.x)
        
    def update(self):
       # update the x value 
       # giving self.rect.right<self.screen_rect.right so that the plane does not move beyond the screen
        if self.moving_right and self.rect.right<self.screen_rect.right:
            self.x +=self.settings.ship_speed
        if self.moving_left and self.rect.left>self.screen_rect.left:
            self.x -=self.settings.ship_speed
        self.rect.x=self.x

    def blitme(self):
        #blit is used to display the image on the screen and make it visible for the user
        self.screen.blit(self.image,self.rect)
        

  
#from pickle import FALSE
import sys
from time import sleep
import pygame
#import random 
from pygame import mixer    
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.settings=Settings()
        self.screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.settings.screen_width=self.screen.get_rect().width
        self.settings.screen_height=self.screen.get_rect().height
        #background music
        mixer.music.load('bgm.mpeg')
        mixer.music.play(-1)
        # giving display name
        pygame.display.set_caption("Alien Invasion")
        self.stats=GameStats(self) 
        self.sb=Scoreboard(self)
        self.ship=Ship(self)
        #calling bullets
        self.bullets=pygame.sprite.Group()
        self.aliens=pygame.sprite.Group()
        self._create_fleet()
        #to create the button
        self.play_button=Button(self,"Play")
        WIN=pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        main_font=pygame.font.SysFont("comicsans",50)
        self.redraw_window(main_font,WIN)
    def redraw_window(self,main_font,WIN):
            
        level_label=main_font.render(f"Level",1,(255,255,255))
        self.screen.blit(level_label,(20,20))
        WIN.blit(level_label,(20,30))
        
    def run_game(self):
        while True:
            self._check_events()
            self.bullets.update()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()


    def _update_bullets(self): 
        #to get rid of the bullets
        for bullet in self.bullets.copy():
            if bullet.rect.bottom<=0:
                self.stats.score -=self.settings.alien_d_points
                self.bullets.remove(bullet)
                
            self.sb.prep_score()
        self._check_bullet_alien_collisions()


    def _check_bullet_alien_collisions(self):
        collisions=pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)
        
        if collisions: 
            colli=mixer.Sound('collisions.mp3')
            colli.play()
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points
             
            self.sb.prep_score()    
        
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet() 
            self.settings.increase_speed()  
            self.stats.level +=1
            self.sb.prep_level()



            
    def _check_events(self):
        for event in pygame.event.get():  
            #responding for key press
                if event.type== pygame.QUIT: 
                    sys.exit()
                

                elif event.type==pygame.MOUSEBUTTONDOWN:
                    mouse_pos=pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)
             
                # checking for down arrow
                elif event.type==pygame.KEYDOWN:
                    self._check_keydown_events(event)

                # checking for up arrow
                elif event.type==pygame.KEYUP:
                    self._check_keyup_events(event)


    def _check_play_button(self,mouse_pos):
        button_clicked= self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.stats.reset_stats()
            self.stats.game_active=True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.aliens.empty()                                                                                                                                                                               
            self.bullets.empty()
            #creating a new fleet and centering the ship
            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)
            self.settings.initialize_dynamic_settings()
     
    def _check_keydown_events(self,event):
        if event.key==pygame.K_RIGHT:
            self.ship.moving_right=True
        elif event.key==pygame.K_LEFT:
            self.ship.moving_left=True
        #To quit the game we need to give q in the keyboard
        elif event.key==pygame.K_q:
            sys.exit()
        #for firing bullets
        elif event.key==pygame.K_SPACE:
            self._fire_bullet()
            bullet_sound=mixer.Sound('gunsound.mp3')
            bullet_sound.play()

    def _check_keyup_events(self,event):
        if event.key==pygame.K_RIGHT:
            self.ship.moving_right=False
        elif event.key==pygame.K_LEFT:
            self.ship.moving_left=False
          
  
    def _fire_bullet(self):
        if len(self.bullets)<self.settings.bullets_allowed:
            new_bullet=Bullet(self)
            self.bullets.add(new_bullet)


    def _create_fleet(self):
            alien=Alien(self)
            alien_width,alien_height=alien.rect.size
            self.aliens.add(alien)  
            alien_width=alien.rect.width
            #checking the available space   
            available_space_x=self.settings.screen_width - (2*alien_width)
            number_aliens_x=(available_space_x//(2*alien_width))-5
            #to find no of rows possible
            ship_height=self.ship.rect.height
            available_space_y=(self.settings.screen_height-(3*alien_height)-ship_height)
            number_rows=(available_space_y//(2*alien_height))-3
            #create first row of of aliens
            for row_number in range(number_aliens_x):
                for alien_number in range(number_aliens_x):
                     self._create_alien(alien_number,row_number)
             

    def _create_alien(self,alien_number,row_number):
        alien=Alien(self)
        alien_width,alien_height=alien.rect.size
        alien.x=alien_width+2*alien_width*alien_number
        alien.rect.x=alien.x
        alien.rect.y=alien.rect.height+2*alien.rect.height*row_number
        self.aliens.add(alien)
        #self._create_fleet()
    
       # self.reset()
        
   # def reset(self):
      #  self.rect.bottom = 0
       # self.rect.centerx = random.randrange(0, 600)
        #self.dy = random.randrange(5, 10)
        #self.dx = random.randrange(-2, 2)


    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien._check_edges():
                self._change_fleet_direction()
                break


    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y+=self.settings.fleet_drop_speed
        self.settings.fleet_direction*=-1


    def _check_aliens_bottom(self):
        screen_rect=self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom>=screen_rect.bottom:
                self._ship_hit()
                break
        


    def _update_aliens(self):

        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()



    def _ship_hit(self):
        if self.stats.ships_left>0:
            self.stats.ships_left -=1
            self.sb.prep_ships()
            self.aliens.empty() 
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.stats.game_active=False
            pygame.mouse.set_visible(True)
   


    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullets()
        self.aliens.draw(self.screen)
        if not self.stats.game_active:
            self.play_button.draw_button()
        self.sb.show_score()
        # to make the changes in the screen everytime the loop is called 
        pygame.display.flip()
    

             
if __name__ =='__main__':
    ai=AlienInvasion()
    ai.run_game()
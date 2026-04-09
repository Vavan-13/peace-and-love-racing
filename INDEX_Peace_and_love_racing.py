import pygame
import time
import random

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
musique = pygame.mixer.music.load("musique.mp3")
musique = pygame.mixer.music.play(-1)
musique = pygame.mixer.music.set_volume(1)
accident_fx = pygame.mixer.Sound("accident.wav")
accident_fx.set_volume(1)

class Game:
    gray = (60, 60, 60)
    black = (255, 0, 0)
    car_width = 90

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Peace and love racing™")
        
        # MODIFICATION ICI : Ajout de pygame.FULLSCREEN et pygame.SCALED
        self.display = pygame.display.set_mode((1400, 850), pygame.FULLSCREEN | pygame.SCALED)
        
        self.score=0
        self.carimg = pygame.image.load("car.png")
        self.position_carimg = self.carimg.get_rect()
        self.position_carimg.center = 45, 95
        self.backgroundleft = pygame.image.load("background.png")
        self.backgroundright = pygame.image.load("background.png")
        self.run()

    def policecar(self, police_startx, police_starty, police):
        if police == 0:
            police_come = pygame.image.load("car2.png")
            position_police_com = self.carimg.get_rect()
        if police == 1:
            police_come = pygame.image.load("car3.png")
            position_police_com = self.carimg.get_rect()
        if police == 2:
            police_come = pygame.image.load("car1.png")
            position_police_com = self.carimg.get_rect()
        self.display.blit(police_come, (police_startx, police_starty))

    def background(self):
        self.display.blit(self.backgroundleft, (0, 0))
        self.display.blit(self.backgroundright, (1400, 0))

    def crash(self):
        self.message_display("Tu t'es crash™!")

    def message_display(self, text):
        large_text = pygame.font.Font("BoldnessRace.ttf", 50)
        musique = pygame.mixer.music.set_volume(0.5)
        accident_fx.play()
        score_text = large_text.render(str(self.score), 1, (0, 0, 0))
        self.display.blit(score_text, (0, 0))
        textsurf, textrect = self.text_object(text, large_text)
        textrect.center = ((700), (300))
        self.display.blit(textsurf, textrect)
        pygame.display.update()
        time.sleep(3)
        musique = pygame.mixer.music.set_volume(1)
        self.loop()

    def text_object(self, text, font):
        text_surface = font.render(text, True, self.black)
        return text_surface, text_surface.get_rect()

    def car(self, x, y):
        self.display.blit(self.carimg, (x, y))

    def loop(self):
        x = 700
        y = 540
        x_change = 0
        y_change = 0
        policecar_speed = 100
        police = random.randint(0,2)
        police_startx = random.randrange(300, (700-self.car_width))
        police_starty = -600
        police_width = 90
        police_height = 90
        self.score = 0
        bumped = False
        while not bumped:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x_change = -10
                    if event.key == pygame.K_RIGHT:
                        x_change = 10
                    # Permet de quitter le plein écran facilement avec ECHAP
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
                        
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        x_change = 0
            x += x_change

            self.display.fill(self.gray)
            self.background()
            police_starty -= (policecar_speed/1.2)
            self.policecar(police_startx, police_starty, police)
            police_starty += policecar_speed
            self.car(x, y)
            
            if x < 325 or x > 1075-self.car_width:
                self.crash()

            if police_starty > 800:
                self.score += 1
                police_starty = 0-police_height
                police_startx = random.randrange(435, (1225-300))
                police = random.randrange(0, 3)

            if y < police_starty+police_height:
                if x > police_startx and x < police_startx + police_width or x + self.car_width > police_startx and x + self.car_width < police_startx + police_width:
                    self.crash()

            pygame.display.update()

    def run(self):
        self.loop()
        pygame.quit()
        quit()

Game()
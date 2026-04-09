import pygame
import asyncio  # 1. Ajout de la bibliothèque asynchrone
import random

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

# Astuce : On met les chargements dans des try/except au cas où 
# un fichier manque, pour éviter que tout le jeu plante d'un coup.
try:
    pygame.mixer.music.load("musique.ogg")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(1)
    accident_fx = pygame.mixer.Sound("accident.ogg")
    accident_fx.set_volume(1)
except FileNotFoundError:
    print("Fichiers audio manquants. Lancement sans le son.")
    accident_fx = None

class Game:
    gray = (60, 60, 60)
    black = (255, 0, 0)
    car_width = 90

    def __init__(self) -> None:
        pygame.display.set_caption("Peace and love racing™")
        self.display = pygame.display.set_mode((1400, 850), pygame.FULLSCREEN | pygame.SCALED)
        self.score = 0
        
        try:
            self.carimg = pygame.image.load("car.png")
            self.backgroundleft = pygame.image.load("background.png")
            self.backgroundright = pygame.image.load("background.png")
        except FileNotFoundError:
            print("Attention : Fichiers images manquants !")
            
        self.position_carimg = self.carimg.get_rect()
        self.position_carimg.center = 45, 95
        
        # 2. On retire self.run() d'ici, on le gère tout en bas via asyncio

    def policecar(self, police_startx, police_starty, police):
        if police == 0:
            police_come = pygame.image.load("car2.png")
        elif police == 1:
            police_come = pygame.image.load("car3.png")
        else:
            police_come = pygame.image.load("car1.png")
            
        self.display.blit(police_come, (police_startx, police_starty))

    def background(self):
        self.display.blit(self.backgroundleft, (0, 0))
        self.display.blit(self.backgroundright, (1400, 0))

    # 3. Les fonctions qui contiennent des pauses doivent devenir 'async'
    async def crash(self):
        await self.message_display("Tu t'es crash™!")

    async def message_display(self, text):
        try:
            large_text = pygame.font.Font("BoldnessRace.ttf", 50)
        except FileNotFoundError:
            large_text = pygame.font.Font(None, 50) # Police par défaut si non trouvée
            
        pygame.mixer.music.set_volume(0.5)
        if accident_fx:
            accident_fx.play()
            
        score_text = large_text.render(str(self.score), 1, (0, 0, 0))
        self.display.blit(score_text, (0, 0))
        textsurf, textrect = self.text_object(text, large_text)
        textrect.center = ((700), (300))
        self.display.blit(textsurf, textrect)
        pygame.display.update()
        
        # 4. Remplacement de time.sleep() qui bloque le navigateur
        await asyncio.sleep(3) 
        
        pygame.mixer.music.set_volume(1)
        await self.loop() # On relance la boucle

    def text_object(self, text, font):
        text_surface = font.render(text, True, self.black)
        return text_surface, text_surface.get_rect()

    def car(self, x, y):
        self.display.blit(self.carimg, (x, y))

    # 5. La boucle principale devient asynchrone
    async def loop(self):
        x = 700
        y = 540
        x_change = 0
        y_change = 0
        
        # Note: 100 pixels de vitesse c'est énorme si on tourne à 60 FPS !
        # Tu devras peut-être réduire cette valeur (ex: 10 ou 15)
        policecar_speed = 100 
        
        police = random.randint(0,2)
        police_startx = random.randrange(300, (700-self.car_width))
        police_starty = -600
        police_width = 90
        police_height = 90
        self.score = 0
        bumped = False
        
        clock = pygame.time.Clock() # 6. Ajout d'une horloge pour réguler la vitesse

        while not bumped:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return # On utilise return pour sortir de l'async au lieu de quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x_change = -10
                    if event.key == pygame.K_RIGHT:
                        x_change = 10
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return 
                        
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
                await self.crash()
                return # On arrête cette boucle car une nouvelle a été lancée

            if police_starty > 800:
                self.score += 1
                police_starty = 0-police_height
                police_startx = random.randrange(435, (1225-300))
                police = random.randrange(0, 3)

            if y < police_starty+police_height:
                if x > police_startx and x < police_startx + police_width or x + self.car_width > police_startx and x + self.car_width < police_startx + police_width:
                    await self.crash()
                    return

            pygame.display.update()
            
            clock.tick(60) # Limite le jeu à 60 images par seconde
            await asyncio.sleep(0) # 7. LA LIGNE MAGIQUE qui rend le jeu web compatible

# 8. Nouvelle méthode de lancement standard pour Pygbag
async def main():
    game = Game()
    await game.loop()

if __name__ == "__main__":
    asyncio.run(main())
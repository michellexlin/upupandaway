#engr 1050, spring 2023, final project
#collaborators: michelle lin and brandon julian gonzalez
# disney movie 'Up' based game 

#import modules
import pygame
import pytmx
import sys
from pytmx.util_pygame import load_pygame
import os

class Game:
    def __init__(self):
        """Initializes game, game window, clocks, etc.
        Inputs: None
        Outputs: None
        Usage: up=Game()
        Returns: None
        """

        #initializes pygame
        pygame.init()

        #sets up working directory
        self.cwd =  os.getcwd()
        self.images = os.path.join(self.cwd,"images")
        self.fonts = os.path.join (self.cwd, "fonts")

        #sets up screen dimensions
        self.window_width = 1440
        self.window_height = 900

        #sets up main game window and popup window
        self.game_window = pygame.display.set_mode((self.window_width, self.window_height))
        self.popup_window = pygame.display.set_mode((self.window_width, self.window_height))
        
        #sets window title to game name
        pygame.display.set_caption("Up Up and Away")

        # Set up the game loop
        self.game_running = True

        #sets up game clock
        self.clock = pygame.time.Clock()

        #loads and scales images used
        self.note = pygame.image.load(f'{self.images}/note.png').convert_alpha()
        self.note_display = pygame.transform.scale(self.note, (32,32))
        self.coinimg=pygame.image.load(f'{self.images}/coin.png').convert_alpha()
        self.coinimg = pygame.transform.scale(self.coinimg,(16,16))
        self.coin_display = pygame.transform.scale(self.coinimg,(25,25))
        self.carlend = pygame.image.load(f'{self.images}/carlend.png').convert_alpha()
        self.ellieend = pygame.image.load(f'{self.images}/ellieend.png').convert_alpha()
        self.heart = pygame.image.load(f'{self.images}/heart.png').convert_alpha()
        self.banner = pygame.image.load(f'{self.images}/banner.png').convert_alpha()
        self.banner = pygame.transform.scale(self.banner, (192,64))
        self.balloon = [pygame.image.load(f'{self.images}/red.png').convert_alpha(), pygame.image.load(f'{self.images}/teal.png').convert_alpha(),pygame.image.load(f'{self.images}/pink.png').convert_alpha(), pygame.image.load(f'{self.images}/orange.png').convert_alpha(), pygame.image.load(f'{self.images}/purple.png').convert_alpha(), pygame.image.load(f'{self.images}/green.png').convert_alpha(), pygame.image.load(f'{self.images}/yellow.png').convert_alpha()]

        #loads and scales images for background
        self.bg5 = pygame.image.load(f'{self.images}/bg5.png').convert_alpha()
        self.bg5 = pygame.transform.scale(self.bg5,(self.window_width, self.window_height))
        self.bg6 = pygame.image.load(f'{self.images}/bg6.png').convert_alpha()
        self.bg6 = pygame.transform.scale(self.bg6,(self.window_width, self.window_height))
        self.bg7 = pygame.image.load(f'{self.images}/bg7.png').convert_alpha()
        self.bg7 = pygame.transform.scale(self.bg7,(self.window_width, self.window_height))
        self.moon = pygame.image.load(f'{self.images}/moon.png').convert_alpha()
        self.moon = pygame.transform.scale(self.moon,(63, 73.5))
        self.water = pygame.image.load(f'{self.images}/blue.png').convert_alpha()
        self.water = pygame.transform.scale(self.water,(self.window_width, self.window_height))

        #load player images for different movements
        self.playerdown = pygame.image.load(f'{self.images}/carl_down_5.png').convert_alpha()
        self.playerup = pygame.image.load(f'{self.images}/carl_up_2.png').convert_alpha()
        self.playerright = pygame.image.load(f'{self.images}/carl_right_3.png').convert_alpha()
        self.playerleft = pygame.image.load(f'{self.images}/carl_left_5.png').convert_alpha()
        self.playerright2 = pygame.image.load(f'{self.images}/carlright.png').convert_alpha()
        self.playerleft2 = pygame.image.load(f'{self.images}/carlleft.png').convert_alpha()

        #sets up rectangles for buttons
        self.nextrec = pygame.Rect(50,510,60,60)
        self.next1rec = pygame.Rect(50,490,80,100)
        self.next2rec = pygame.Rect(50,490,80,95)
        self.next3rec = pygame.Rect(50,490,80,95)
        self.startrec = pygame.Rect(670,398,108,35)
        self.exitrec = pygame.Rect (680,498,90,35)
        self.exit1rec = pygame.Rect(1350,10,70,95)
        self.exit2rec = pygame.Rect(1350,10,70,95)
        self.exit3rec = pygame.Rect(1350,10,70,95)
        self.exit4rec = pygame.Rect(1350,10,70,95)

        #sets initial direction player is facing and jump count
        self.direction = 'down'
        self.jump_counter=0

        #sets game fonts and relevant times
        self.font = pygame.font.Font(f'{self.fonts}/pix.ttf', 18)
        self.menufont = pygame.font.Font(f'{self.fonts}/chub.ttf', 100)
        self.font2 = pygame.font.Font(f'{self.fonts}/pix.ttf', 35)
        self.FPS=30
        self.playtime=0.0
        self.pfplaytime=0.0
        self.remainingtime=0.0
        self.pfremainingtime=0.0
        
        #initializes levels
        self.leveloneinit()
        self.leveltwoinit()
        self.levelthreeinit()

        #sets initial state to be the menu screen
        self.state = 'menu'
        
    def state_manager(self):
        """Checks game state and changes when necessary
        Inputs: None
        Outputs: None
        Usage: self.state_manager()
        Returns: None
        """
        #checks state and runs cooresponding method
        if self.state == 'menu':
            self.menu()
        if self.state == 'levelonestart':
            self.levelonestart()
        if self.state == 'levelone':
            self.levelone()
        if self.state == 'leveltwostart':
            self.leveltwostart()
        if self.state=='leveltwo':
            self.leveltwo()
        if self.state=='levelthree':
            self.levelthree()

    def mouse_click(self):
        """Checks whether button was clicked
        Inputs: None
        Outputs: None
        Usage: self.mouse_click()
        Returns: None
        """
        #gets coordinates of mouse
        self.mousex, self.mousey = pygame.mouse.get_pos()

        #checks state of game
        if self.state == 'menu':
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        #checks if click is over start or exit button
                        if self.startrec.collidepoint(self.mousex,self.mousey):
                            self.state='levelonestart'
                        elif self.exitrec.collidepoint(self.mousex,self.mousey):
                            self.game_running = False
                            pygame.quit()
                            sys.exit()

        elif self.state == 'levelonestart':
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        #checks if mouse click is over arrow button
                        if self.nextrec.collidepoint(self.mousex,self.mousey):
                            self.state='levelone'

        elif self.state == 'levelone':
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        #checks if mouse click is over arrow button
                        if self.next1rec.collidepoint(self.mousex,self.mousey):
                            self.state='leveltwostart'
                        if self.exit1rec.collidepoint(self.mousex,self.mousey):
                            self.game_running = False
                            pygame.quit()
                            sys.exit()

        elif self.state == 'leveltwostart':
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        #checks if mouse click is over arrow button
                        if self.next2rec.collidepoint(self.mousex,self.mousey):
                            self.state='leveltwo'
                        #checks if mouse click is over x
                        elif self.exit2rec.collidepoint(self.mousex,self.mousey):
                            self.game_running = False
                            pygame.quit()
                            sys.exit()

        elif self.state == 'leveltwo':
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        #checks if mouse click is over arrow button
                        if self.next3rec.collidepoint(self.mousex,self.mousey):
                            self.state='levelthree'
                        #checks if mouse click is over x
                        elif self.exit3rec.collidepoint(self.mousex,self.mousey):
                            self.game_running = False
                            pygame.quit()
                            sys.exit()

        elif self.state == 'levelthree':
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        #checks if mouse click is over x
                        if self.exit4rec.collidepoint(self.mousex,self.mousey):
                            self.game_running = False
                            pygame.quit()
                            sys.exit()

    def menu(self):
        """Sets up start menu
        Inputs: None
        Outputs: None
        Usage: self.menu()
        Returns: None
        """
        #sets background for menu screen
        self.game_window.blit(self.bg1, (0,0))
        self.game_window.blit(self.bg2, (0,0))
        self.game_window.blit(self.bg3, (0,0))
        self.game_window.blit(self.bg4, (0,0))

        #sets title and balloon images
        self.menutitle = self.menufont.render("Up Up and Away", True, ('White'))
        self.game_window.blit(self.menutitle, (330, 160))
        self.game_window.blit(self.balloon[0], (330,140))
        self.game_window.blit(self.balloon[1], (350,150))
        self.game_window.blit(self.balloon[2], (1000,160))
        self.game_window.blit(self.balloon[3], (1030,170))
        self.game_window.blit(self.balloon[5], (1040,155))

        #sets text for start and exit buttons
        self.menu1_surface = self.font2.render("Start", True, ('White'))
        self.game_window.blit(self.menu1_surface, (670,400))
        self.menu1_surface = self.font2.render("Exit", True, ('White'))
        self.game_window.blit(self.menu1_surface, (680,500))

        #checks where mouse is clicked
        self.mouse_click()

    def leveloneinit(self):
        """Initializes level one map/map layers and relevant images
        Inputs: None
        Outputs: None
        Usage: up=Game(), up.leveloneinit()
        Returns: None
        """
        #load tiled map and sets tile dimensions
        self.tiled_map = load_pygame("home.tmx")
        self.tilewidth = self.tiled_map.tilewidth
        self.tileheight = self.tiled_map.tileheight

        #gets layers within tiled map
        self.collision = self.tiled_map.get_layer_by_name('collisions')
        self.foreground = self.tiled_map.get_layer_by_name('foreground')
        self.foreground2 = self.tiled_map.get_layer_by_name('foreground2')
        self.collectibles = self.tiled_map.get_layer_by_name("Collectibles")

        #sets list of tiles to be tiles marked as collision tiles (tiles player can't walk through)
        self.tiles = []
        for x, y, tile in self.collision.tiles():
            if tile:
                self.tiles.append(pygame.Rect(x * self.tilewidth, y * self.tileheight, self.tilewidth, self.tileheight))

        #sets initial count for collectible notes
        self.notecount=0

        #Create a list of collectables
        self.objects = self.tiled_map.get_layer_by_name('Collectibles')
        self.items = []
        for object in self.objects:
            self.items.append(object)

    def leveltwoinit(self):
        """Initializes level two map/map layers and relevant images
        Inputs: None
        Outputs: None
        Usage: self.leveltwoinit()
        Returns: None
        """
        #load tiled map and sets tile dimensions
        self.platform_map = load_pygame("grass.tmx")
        self.pftilewidth = self.platform_map.tilewidth
        self.pftileheight = self.platform_map.tileheight

        #gets layers within tiled map
        self.pfcollision = self.platform_map.get_layer_by_name('collisions')
        self.pfcollectibles = self.platform_map.get_layer_by_name("collectibles")

        #sets list of tiles to be tiles marked as collision tiles (tiles player can't walk through)
        self.pftiles = []
        for x, y, tile in self.pfcollision.tiles():
            if tile:
                self.pftiles.append(pygame.Rect(x * self.pftilewidth, y * self.pftileheight, self.pftilewidth, self.pftileheight))

        #loads and scales images for background
        self.bg1 = pygame.image.load(f'{self.images}/bg1.png').convert_alpha()
        self.bg1 = pygame.transform.scale(self.bg1,(self.window_width, self.window_height))
        self.bg2 = pygame.image.load(f'{self.images}/bg2.png').convert_alpha()
        self.bg2 = pygame.transform.scale(self.bg2,(self.window_width, self.window_height))
        self.bg3 = pygame.image.load(f'{self.images}/bg3.png').convert_alpha()
        self.bg3 = pygame.transform.scale(self.bg3,(self.window_width, self.window_height))
        self.bg4 = pygame.image.load(f'{self.images}/bg4.png').convert_alpha()
        self.bg4 = pygame.transform.scale(self.bg4,(self.window_width, self.window_height))
        self.grassbg = pygame.image.load(f'{self.images}/greenbg.png').convert_alpha()
        self.grassbg=pygame.transform.scale(self.grassbg,(self.window_width,self.window_height))

        #sets initial falling condition to false
        self.falling = False

        #Create a list of collectables
        self.coin = self.platform_map.get_layer_by_name('collectibles')
        self.coins = []
        for object in self.coin:
            self.coins.append(object)

        #sets initial coin count
        self.coincount = 0

    def levelthreeinit(self):
        """Initializes level three map/map layers and relevant images
        Inputs: None
        Outputs: None
        Usage: self.levelthreeinit()
        Returns: None
        """
        #load tiled map and sets tile dimensions
        self.end_map = load_pygame("end.tmx")

        #gets layers within tiled map
        self.endcollision = self.end_map.get_layer_by_name('collisions')
        self.endforeground = self.end_map.get_layer_by_name('foreground')

    def levelonestart(self):
        """Displays message before start of level one
        Inputs: None
        Outputs: None
        Usage: self.levelonestart()
        Returns: None
        """
        #sets background images
        self.game_window.blit(self.bg1, (0,0))
        self.game_window.blit(self.bg2, (0,0))
        self.game_window.blit(self.bg3, (0,100))
        self.game_window.blit(self.bg4, (0,0))

        #sets text on screen
        self.welcome1_surface = self.font.render("Welcome!", True, ('White'))
        self.game_window.blit(self.welcome1_surface, (50,250))
        self.welcome2_surface = self.font.render("This game is (very) loosely based on Pixar's Up.", True, ('White'))
        self.game_window.blit(self.welcome2_surface, (50,310))
        self.welcome3_surface = self.font.render("You'll play as Carl Fredrickson, trying to get to his wife Ellie before she dies!", True, ('White'))
        self.game_window.blit(self.welcome3_surface, (50,350))
        self.welcome4_surface = self.font.render("In this first level, collect the notes scattered around the house to get the key to the front door.", True, ('White'))
        self.game_window.blit(self.welcome4_surface, (50,390))
        self.welcome4_surface = self.font.render("Be careful, you're under a time crunch. Wouldn't want Ellie to die all alone...", True, ('White'))
        self.game_window.blit(self.welcome4_surface, (50,430))
        
        #creates arrow to move to next scenes
        self.welcome5_surface = self.menufont.render("-", True, ('White'))
        self.game_window.blit(self.welcome5_surface, (50,490))
        self.welcome6_surface = self.menufont.render(">", True, ('White'))
        self.game_window.blit(self.welcome6_surface, (68,490))

        #sets playtime
        self.milliseconds = self.clock.tick(self.FPS)
        self.playtime += self.milliseconds / 1000.0

        #checks where mouse is clicked
        self.mouse_click()

    def leveltwostart(self):
        """Displays message before start of level two
        Inputs: None
        Outputs: None
        Usage: self.leveltwostart()
        Returns: None
        """
        #sets background images
        self.game_window.blit(self.bg5, (0,0))
        self.game_window.blit(self.bg6, (0,0))
        self.game_window.blit(self.bg7, (0,0))
        self.game_window.blit(self.moon, (1300,100))

        #sets text on screen
        self.welcome1_surface = self.font.render("You decide to follow the map to Paradise Falls, hoping Ellie is there.", True, ('white'))
        self.game_window.blit(self.welcome1_surface, (50,250))
        self.welcome2_surface = self.font.render("In this level, traverse the jungle to make it through.", True, ('white'))
        self.game_window.blit(self.welcome2_surface, (50,310))
        self.welcome3_surface = self.font.render("Collect some coins while you're at it. You can throw it in the rainy day fund.", True, ('white'))
        self.game_window.blit(self.welcome3_surface, (50,350))
        self.welcome4_surface = self.font.render("Be careful, wouldn't want Ellie to die all alone...", True, ('white'))
        self.game_window.blit(self.welcome4_surface, (50,390))
        
        #sets arrow for next scenes
        self.welcome5_surface = self.menufont.render("-", True, ('White'))
        self.game_window.blit(self.welcome5_surface, (50,490))
        self.welcome6_surface = self.menufont.render(">", True, ('White'))
        self.game_window.blit(self.welcome6_surface, (68,490))

        #sets playtime
        self.pfmilliseconds = self.clock.tick(self.FPS)
        self.pfplaytime += self.pfmilliseconds / 1000.0

        #checks where mouse is clicked
        self.mouse_click()
        
    def levelone(self):
        """"Game Level One
        Inputs: None
        Outputs: None
        Usage: self.levelone()
            Returns: Level one of game displayed
        """
        #fills background with green
        self.game_window.blit(self.grassbg,(0,0))

        #sets game camera to follow player object
        self.CAMERA = self.tiled_map.get_object_by_name("Player")

        #render map tiles and objects
        for layer in self.tiled_map.layers:
            if isinstance(layer, pytmx.TiledTileLayer) and (layer != self.collision) and (layer!=self.foreground) and (layer!=self.foreground2):
                for x, y, tile in layer.tiles():
                    if (tile):
                        self.game_window.blit(tile, [(x * self.tilewidth)-self.CAMERA.x+(self.window_width/2), (y * self.tileheight)-self.CAMERA.y+(self.window_height/2)])

                #displays character image based on direction of movement
                if self.direction == 'down':
                    self.game_window.blit(self.playerdown, [(self.tiled_map.get_object_by_name("Player").x)-self.CAMERA.x +(self.window_width/2) , (self.tiled_map.get_object_by_name("Player").y)-self.CAMERA.y +(self.window_height/2)])
                elif self.direction == 'up':
                    self.game_window.blit(self.playerup, [(self.tiled_map.get_object_by_name("Player").x)-self.CAMERA.x +(self.window_width/2) , (self.tiled_map.get_object_by_name("Player").y)-self.CAMERA.y +(self.window_height/2)])
                if self.direction == 'left':
                    self.game_window.blit(self.playerleft2, [(self.tiled_map.get_object_by_name("Player").x)-self.CAMERA.x +(self.window_width/2) , (self.tiled_map.get_object_by_name("Player").y)-self.CAMERA.y +(self.window_height/2)])
                elif self.direction == 'right':
                    self.game_window.blit(self.playerright2, [(self.tiled_map.get_object_by_name("Player").x)-self.CAMERA.x +(self.window_width/2) , (self.tiled_map.get_object_by_name("Player").y)-self.CAMERA.y +(self.window_height/2)])

            #renders collectible objects
            elif isinstance(layer, pytmx.TiledObjectGroup) and (layer == self.collectibles): 
                for object in (layer and self.items):
                    self.game_window.blit(self.note, [object.x-self.CAMERA.x+(self.window_width/2) , object.y-self.CAMERA.y+(self.window_height/2)])

        #sets initial position of player            
        self.pos = [0, 0]

        #defines player movements
        self.movement()
        
        #renders foreground layers so they are in front of the player
        for layer in self.tiled_map.layers:
            if isinstance(layer, pytmx.TiledTileLayer) and ((layer == self.foreground) or layer == self.foreground2):
                for x, y, tile in layer.tiles():
                    if (tile):
                        self.game_window.blit(tile, [(x * self.tilewidth)-self.CAMERA.x+(self.window_width/2), (y * self.tileheight)-self.CAMERA.y+(self.window_height/2)])
        
        #creates rectangle for player
        self.player_rec()

        #checks if player rectangle collides with collision tiles and cancels movement if true
        if(self.checkbounds()):
            self.pos = [0,0]
        
        #changes position based on movement
        self.tiled_map.get_object_by_name("Player").x += self.pos[0]
        self.tiled_map.get_object_by_name("Player").y += self.pos[1]

        #check collectibles with the current position of the player
        self.checknotes(pygame.Rect([self.tiled_map.get_object_by_name("Player").x,self.tiled_map.get_object_by_name("Player").y, self.tiled_map.get_object_by_name("Player").width,self.tiled_map.get_object_by_name("Player").height]))
        
        #sets note image for note counter and renders numbers based on current collected note count
        self.game_window.blit(self.note_display, (10,10))
        self.note_counter()

        #displays remaining time in level
        self.time_counter(60)

        #checks conditions to end the level
        self.level_end()

    def checknotes(self, playerrec):
        """Checks whether or not a note has been collected by the player
        Inputs: playerrec
        Outputs: None
        Usage: self.checknotes(playerrec)
            Returns: None
        """
        #creates list of notes that player has collected
        collected_indices = []
        for i, item in enumerate(self.items):
            #creates rectangle for each note
            noterec = pygame.Rect([item.x, item.y, item.width, item.height])
            #checks if player has collided with note rectangle and if the note is visible on the screen
            if noterec.colliderect(playerrec) and item.visible:
                #makes note invisible, adds to collected item list and increases note count
                item.visible = 0
                collected_indices.append(i)
                self.notecount = self.notecount+1

        #removes item from collected list
        for i in reversed(collected_indices):
            self.items.pop(i)

    def note_counter(self):
        """"displays collected note count
        Inputs: None
        Outputs: None
        Usage: self.note_counter()
            Returns: None
        """
        #sets note image for note counter
        self.game_window.blit(self.banner, (2,2))
        self.game_window.blit(self.note_display, (13,21))
        self.game_window.blit(self.banner, (2,66))

        #renders numbers based on current collected note count
        self.note_surface = self.font.render(f"{self.notecount}", True, ('white'))
        self.game_window.blit(self.note_surface, (45,35))
        
    def time_counter(self,timestart):
        """"displays time left in level
        Inputs: timestart (int)
        Outputs: None
        Usage: self.time_counter()
            Returns: None
        """        
        #checks that level is not over based on collectibles
        if self.notecount!=4:
            #displays remaining time on to screen
            self.remainingtime = max(0, timestart - self.playtime)
            self.time_surface = self.font.render("{1:.2f} seconds".format(self.FPS, self.remainingtime), True, ('white'))
        self.game_window.blit(self.time_surface, (27, 98))

    def checkbounds(self):
        """Checks whether or not player is collided with the bounds
        Inputs: playerrec
        Outputs: True or Fales
        Usage: self.checkbounds(playerrec)
            Returns: True/False
        """
        # checks if player has collided with tiles in the list of collision tiles and returns boolean
        check = False
        if self.playerrec.collidelistall(self.tiles):
            check = True
        return check
    
    def movement(self):
        """"Checks what keys are being pressed and moves the player accordingly
        Inputs: None
        Outputs: None
        Usage: self.movement()
            Returns: Player in new position
        """
        #checks which keys are pressed and moves player accordingly
        PRESSED=pygame.key.get_pressed()

        #moves player 2 units in direction of key press and changes character direction
        if PRESSED[pygame.K_LEFT]:
            self.pos[0] -= 2
            self.direction = 'left'
        elif PRESSED[pygame.K_RIGHT]:
            self.pos[0] += 2
            self.direction = 'right'

        if PRESSED[pygame.K_UP]:
            self.pos[1] -= 2
            self.direction = 'up'
        elif PRESSED[pygame.K_DOWN]:
            self.pos[1] += 2
            self.direction = 'down'

    def player_rec(self):
        """"creates rectangle for player
        Inputs: None
        Outputs: None
        Usage: self.player_rec()
            Returns: None
        """
        #creates and updates rectangle for player based on original position and key presses
        self.x = self.tiled_map.get_object_by_name("Player").x + self.pos[0]
        self.y = self.tiled_map.get_object_by_name("Player").y + self.pos[1]
        self.w = self.tiled_map.get_object_by_name("Player").width
        self.h = self.tiled_map.get_object_by_name("Player").height
        self.playerrec = pygame.Rect([self.x, self.y, self.w, self.h])

    def leveltwo(self):
        """"Game Level two
        Inputs: None
        Outputs: None
        Usage: self.leveltwo()
            Returns: Level two of game displayed
        """
        #sets images for background
        self.game_window.blit(self.bg5, (0,0))
        self.game_window.blit(self.bg6, (0,0))
        self.game_window.blit(self.bg7, (0,0))
        self.game_window.blit(self.moon, (1300,100))

        #sets game camera to follow player object
        self.pfCAMERA = self.platform_map.get_object_by_name("Player")
        
        #render map tiles and objects
        for layer in self.platform_map.layers:
            if isinstance(layer, pytmx.TiledTileLayer) and (layer != self.pfcollision):
                for x, y, tile in layer.tiles():
                    if (tile):
                        self.game_window.blit(tile, [(x * self.pftilewidth)-self.pfCAMERA.x+(self.window_width/2), (y * self.pftileheight)])

                #renders different player images based on direction player moves
                if self.direction == 'left':
                    self.game_window.blit(self.playerleft, [(self.platform_map.get_object_by_name("Player").x)-self.pfCAMERA.x +(self.window_width/2) , (self.platform_map.get_object_by_name("Player").y)])
                elif self.direction =='right':
                    self.game_window.blit(self.playerright, [(self.platform_map.get_object_by_name("Player").x)-self.pfCAMERA.x +(self.window_width/2) , (self.platform_map.get_object_by_name("Player").y ) ])

            #renders collectible objects
            elif isinstance(layer, pytmx.TiledObjectGroup) and (layer == self.pfcollectibles): 
                for object in (layer and self.coins):
                    self.game_window.blit(self.coinimg, [object.x-self.pfCAMERA.x+(self.window_width/2) , object.y])

        #sets initial position of player            
        self.pfpos=[0,0]

        #defines movements on platforms
        self.platformmovement()

        #implements gravity
        self.gravity()

        #creates rectangle for player
        self.player_pfrec()

        #checks if player collides with collision tiles and cancels movement if true, sets falling to false if collision occurs
        if(self.checkpfbounds()):
            self.pfpos = [0,0]
            self.falling=False
        #if collision doesn't occur, continue falling
        else:
            self.falling=True

        #updates location based on initial position and keypress
        self.platform_map.get_object_by_name("Player").x += self.pfpos[0]
        self.platform_map.get_object_by_name("Player").y += self.pfpos[1]

        #checks if coins are picked up based on player rectangle
        self.checkcoins(pygame.Rect([self.platform_map.get_object_by_name("Player").x,self.platform_map.get_object_by_name("Player").y, self.platform_map.get_object_by_name("Player").width,self.platform_map.get_object_by_name("Player").height]))
        
        #displays coin count
        self.coin_counter()

        #checks whether level ending conditions have been met
        self.level_end()

    def checkcoins(self,playerrec):
        """"checks if coins are picked up
        Inputs: playerrec
        Outputs: None
        Usage: self.checkcoins()
            Returns: None
        """
        #creates empty list for collected coins
        collected_coins = []
        for i, item in enumerate(self.coins):
            #creates rectangle for each coin
            coinrec = pygame.Rect([item.x, item.y, item.width, item.height])
            #checks if player has collided with coin rectangle and if the coin is visible on the screen
            if coinrec.colliderect(playerrec) and item.visible:
                #makes coin invisible, adds to collected item list and increases coin count
                item.visible = 0
                collected_coins.append(i)
                self.coincount = self.coincount+1
        #removes item from collected list
        for i in reversed(collected_coins):
            self.coins.pop(i)

    def coin_counter(self):
        """"displays number of coins collected
        Inputs: None
        Outputs: None
        Usage: self.coin_counter()
            Returns: None
        """
        #displays images and current coin count
        self.game_window.blit(self.banner, (2,2))
        self.game_window.blit(self.coin_display, (16,30))
        self.coin_surface = self.font.render(f"{self.coincount}", True, ('white'))
        self.game_window.blit(self.coin_surface,(47,35))

    def player_pfrec(self):
        """"creates rectangle for player
        Inputs: None
        Outputs: None
        Usage: self.pfplayer_rec()
            Returns: None
        """
        #creates rectangle for player
        self.pfx = self.platform_map.get_object_by_name("Player").x + self.pfpos[0]
        self.pfy = self.platform_map.get_object_by_name("Player").y + self.pfpos[1]
        self.pfw = self.platform_map.get_object_by_name("Player").width
        self.pfh = self.platform_map.get_object_by_name("Player").height
        self.pfplayerrec = pygame.Rect([self.pfx, self.pfy, self.pfw, self.pfh])

    def platformmovement(self):
        """"defines player movements
        Inputs: None
        Outputs: None
        Usage: self.platformmovement()
            Returns: None
        """
        # checks which keys are pressed and moves player accordingly
        PRESSED=pygame.key.get_pressed()

        #moves player based on key press and changes player direction
        if PRESSED[pygame.K_LEFT]:
            self.pfpos[0] -= 5
            self.direction = 'left'
            self.jump_counter=0
            
        elif PRESSED[pygame.K_RIGHT]:
            self.pfpos[0] += 5
            self.direction = 'right'
            self.jump_counter=0
        
        #checks how many times up key has been pressed (prevents floating over obstacles)
        #if up is pressed, set falling to true and increasing jump counter
        if self.jump_counter<=3:
            if PRESSED[pygame.K_UP]:
                self.falling=True
                self.pfpos[1]-=10
                self.jump_counter+=1

    def gravity(self):
        """"implements "gravity"
        Inputs: None
        Outputs: None
        Usage: self.gravity()
            Returns: None
        """
        #checks if falling condition is true
        if self.falling==True:
            #moves player down
            self.pfpos[1]+=5

    def checkpfbounds(self):
        """Checks whether or not player is collided with the bounds
        Inputs: playerrec
        Outputs: True or Fales
        Usage: self.checkbounds(playerrec)
            Returns: True/False
        """
        # checks if player has collided with tiles in the list of collision tiles and returns boolean values
        check = False
        if self.pfplayerrec.collidelistall(self.pftiles):
            check = True
        return check
    
    def levelthree(self):
        """"Game Level two
        Inputs: None
        Outputs: None
        Usage: self.leveltwo()
            Returns: Level two of game displayed
        """
        #sets background image
        self.game_window.blit(self.water, (0,0))

        #sets game camera to follow player object
        self.endCAMERA = self.end_map.get_object_by_name("Player")

        #render map tiles and objects
        for layer in self.end_map.layers:
            if isinstance(layer, pytmx.TiledTileLayer) and (layer != self.endcollision) and (layer!=self.endforeground):
                for x, y, tile in layer.tiles():
                    if (tile):
                        self.game_window.blit(tile, [(x * self.pftilewidth), (y * self.pftileheight)])

                    #renders carl and ellie images
                    self.game_window.blit(self.carlend, [(self.end_map.get_object_by_name("Player").x) , (self.end_map.get_object_by_name("Player").y)])
                    self.game_window.blit(self.ellieend, [(self.end_map.get_object_by_name("Ellie").x) , (self.end_map.get_object_by_name("Ellie").y)])

        #renders foreground layers so they are in front of the player
        for layer in self.end_map.layers:
            if isinstance(layer, pytmx.TiledTileLayer) and (layer == self.endforeground):
                for x, y, tile in layer.tiles():
                    if (tile):
                        self.game_window.blit(tile, [(x * self.pftilewidth), (y * self.pftileheight)])

        #render images for heart icon and x to close game
        self.game_window.blit(self.heart, (693,505))
        self.text5_surface = self.menufont.render("x", True, ('White'))
        self.game_window.blit(self.text5_surface, (1350,10))

        #checks where mouse has been clicked
        self.mouse_click()

    def level_end(self):
        #checks what level user is currently on
        if self.state =='levelone':
            #checks whether all collectibles have been picked up
            if (self.notecount==4):

                #displays background images
                self.game_window.blit(self.bg1, (0,0))
                self.game_window.blit(self.bg2, (0,0))
                self.game_window.blit(self.bg3, (0,0))
                self.game_window.blit(self.bg4, (0,0))

                #displays end message
                self.text1_surface = self.font.render("You found all the notes, yay!", True, ('white'))
                self.game_window.blit(self.text1_surface, (50,250))
                self.text2_surface = self.font.render("They lead you to the key out.", True, ('white'))
                self.game_window.blit(self.text2_surface, (50,290))
                self.text3_surface = self.font.render("You also find a map leading you to Paradise Falls.", True, ('white'))
                self.game_window.blit(self.text3_surface, (50,330))

                #displays arrow to move to next scenes
                self.welcome5_surface = self.menufont.render("-", True, ('White'))
                self.game_window.blit(self.welcome5_surface, (50,490))
                self.welcome6_surface = self.menufont.render(">", True, ('White'))
                self.game_window.blit(self.welcome6_surface, (68,490))

                #check where mouse has been clicked
                self.mouse_click()
                
            #checks if time has run out
            elif (self.remainingtime == 0.0):

                #displays background images
                self.game_window.blit(self.bg1, (0,0))
                self.game_window.blit(self.bg2, (0,0))
                self.game_window.blit(self.bg3, (0,0))
                self.game_window.blit(self.bg4, (0,0))

                #displays end messages
                self.text1_surface = self.font.render("You ran out of time and did not collect the notes.", True, ('white'))
                self.game_window.blit(self.text1_surface, (50,250))

                #checks notecount to display cooresponding messages
                if (4-self.notecount)==1:
                    self.text2_surface = self.font.render(f"You had {4 - self.notecount} note remaining.", True, ('white'))
                    self.game_window.blit(self.text2_surface, (50,290))
                else: 
                    self.text2_surface = self.font.render(f"You had {4 - self.notecount} notes remaining.", True, ('white'))
                    self.game_window.blit(self.text2_surface, (50,290))
                self.text3_surface = self.font.render("You wasted too much time and Ellie died, sad and alone :(", True, ('white'))
                self.game_window.blit(self.text3_surface, (50,330))
                self.text4_surface = self.font.render("That guilt consumes you, and you die shortly after, also all alone.", True, ('white'))
                self.game_window.blit(self.text4_surface, (50,370))

                #display x to close game
                self.text5_surface = self.menufont.render("x", True, ('White'))
                self.game_window.blit(self.text5_surface, (1350,10))

                #check where mouse is clicked
                self.mouse_click()

        elif self.state == 'leveltwo':
            #checks if character has fallen below screen
            if self.pfy>=self.window_height:
                #displays background image
                self.game_window.blit(self.bg5, (0,0))
                self.game_window.blit(self.bg6, (0,0))
                self.game_window.blit(self.bg7, (0,0))
                self.game_window.blit(self.moon, (1300,100))

                #displays end message
                self.text1_surface = self.font.render("Unfortunately, you fell to your death :/", True, ('white'))
                self.game_window.blit(self.text1_surface, (50,250))
                self.text2_surface = self.font.render("Ellie once said you were getting slow for your age. I guess that's true after all.", True, ('white'))
                self.game_window.blit(self.text2_surface, (50,290))
                self.text3_surface = self.font.render("Sadly, she died all alone wondering where you were.", True, ('white'))
                self.game_window.blit(self.text3_surface, (50,330))

                #display x to close game
                self.text4_surface = self.menufont.render("x", True, ('White'))
                self.game_window.blit(self.text4_surface, (1350,10))

                #checks where mouse is clicked
                self.mouse_click()
            
            #checks that all coins have been collected
            elif (self.coincount==20):
                #displays background images
                self.game_window.blit(self.bg5, (0,0))
                self.game_window.blit(self.bg6, (0,0))
                self.game_window.blit(self.bg7, (0,0))
                self.game_window.blit(self.moon, (1300,100))

                #displays end message
                self.text1_surface = self.font.render("You made it through Paradise Falls!", True, ('white'))
                self.game_window.blit(self.text1_surface, (50,250))
                self.text2_surface = self.font.render("Ellie should be waiting for you on the other side.", True, ('white'))
                self.game_window.blit(self.text2_surface, (50,290))
                self.text3_surface = self.font.render("Go ahead, click to continue.", True, ('white'))
                self.game_window.blit(self.text3_surface, (50,330))

                #displays arrow to go to next scenes
                self.text4_surface = self.menufont.render("-", True, ('White'))
                self.game_window.blit(self.text4_surface, (50,490))
                self.text5_surface = self.menufont.render(">", True, ('White'))
                self.game_window.blit(self.text5_surface, (68,490))

                #checks where mouse has been clicked
                self.mouse_click()

    def game_loop(self):
        #contines running while game_running is true
        while self.game_running:
            #handle events
            for event in pygame.event.get():
                #ends game if user exits
                if event.type == pygame.QUIT:
                    self.game_running = False

            #sets playtime
            milliseconds = self.clock.tick(self.FPS) 
            self.playtime += milliseconds / 1000.0

            #checks and changes actibe states
            self.state_manager()

            #updates display
            pygame.display.update()
        #quit event to end game
        pygame.quit()
        sys.exit()

#creates game object and runs game loop
up=Game()
up.game_loop()

    
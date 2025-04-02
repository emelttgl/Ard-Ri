import pygame
from pygame.locals import *
from board import Board
import player as pl
from player import HumanPlayer, AIPlayer

DEPTH = 3 

class Game:

    def __init__(self, length, width):
        
        self.window = pygame.display.set_mode((length, width))
        pygame.display.set_caption('ARD-RI')
        logo = pygame.image.load('images/titles/logo.png')
        pygame.display.set_icon(logo)
    

        # Images 
        self.background = pygame.image.load("images/background1.jpg")
        self.subtitle = pygame.image.load("images/titles/subtitle.png")
        self.move = pygame.image.load("images/pawns/move.png")
        self.b_victory = pygame.image.load("images/titles/b_victory.png")
        self.w_victory = pygame.image.load("images/titles/w_victory.png")
       
        # Création du plateau
        board_model = [
            [0, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [1, 0, 2, 2, 2, 0, 1],
            [1, 1, 2, 3, 2, 1, 1],
            [1, 0, 2, 2, 2, 0, 1],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 1, 1, 1, 0, 0],
        ]
        self.board = Board(board_model)

        self.status = False

        self.is_on_menu = True
        self.is_on_party = False
        self.is_on_results = False

        self.human_player = HumanPlayer('white')
        self.ai_player = AIPlayer('black', False)
        self.current_player = self.human_player

       

    def get_mouse_position(self):     
        mouse = pygame.mouse.get_pos()#renvoi de la case ou se trouve la souris
        mouse_x = mouse[0]
        mouse_y = mouse[1]
        for x in range(7):
            for y in range(7):
                if x * 100 + 100 >= mouse_x and x * 100 + 100 < mouse_x + 100 and y * 100 + 100 >= mouse_y and y * 100 + 100 < mouse_y + 100:
                    return (x,y)

    def menu(self):
        self.window.blit(self.background, (0, 0))# Menu 
        self.window.blit(self.subtitle, (120,300))
            

    def party(self, event):
        
        if event.type == MOUSEBUTTONDOWN:
            self.status = self.board.update(self.get_mouse_position())
        self.board.display(self.window, self.get_mouse_position())


        '''if self.board.is_black_turn:
            self.status = self.board.update(ia.make_move(self.board))
        else:
            if event.type == MOUSEBUTTONDOWN:
                self.status = self.board.update(self.get_mouse_position())
        self.board.display(self.window, self.get_mouse_position())'''


    def results(self):
        self.window.blit(self.background, (0, 0))#affichage des resultats
        if self.status == "b":
            self.window.blit(self.b_victory, (170, 200))
        if self.status == "w":
            self.window.blit(self.w_victory, (170, 200))

    def run(self):
        lock = True
        while lock:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    lock = False

                if self.is_on_menu: # Gestion du menu
                    self.menu()
                    if event.type == KEYDOWN and event.key == K_SPACE:
                        self.is_on_menu = False
                        self.is_on_party = True

                if self.is_on_party: # Gestion de la partie
                    self.party(event)
                    if self.status == "w" or self.status == "b":
                        self.is_on_results = True
                        self.is_on_party = False
                        self.results()

                if self.is_on_results: # Gestion des résultats
                    self.results()
                    if event.type == KEYDOWN and event.key == K_SPACE:
                        self.__init__(700,700)

            pygame.display.update()

        pygame.quit()

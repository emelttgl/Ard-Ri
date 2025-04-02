import pygame

class Move:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.surface = pygame.image.load("images/pawns/move.png")

    def get_coord(self):
        #les coordonnées mouvement possible
        return (self.x, self.y)

    def set_coord(self, coords):
        #Affichage des coordonnées mouvement possible
        self.x = coords[0]
        self.y = coords[1]

    def draw(self, window):
        #Affichage pygame du mouvement possible'''
        if self.get_coord() != (3,3):
            window.blit(self.surface, (self.x * 100 + 31, self.y * 100 + 31)) # on met +1 pour les lignes 
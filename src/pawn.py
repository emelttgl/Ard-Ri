import pygame

class Pawn:

    def __init__(self, team, x, y):
        self.team = team
        self.x = x
        self.y = y
        self.surface = pygame.image.load(f"images/pawns/{team}.png")
        self.surface_hover = pygame.image.load(f"images/pawns/{team}_hover.png")
        self.is_hover = False

    def get_coord(self):
        #coordonnées du pion 
        return (self.x, self.y)

    def set_coord(self, coords):
        #modification des coord du pion
        self.x = coords[0]
        self.y = coords[1]

    def set_hover(self, mouse):
        #determine si la souris se situe au dessus du jeton
        if self.get_coord() == mouse:
            self.is_hover = True
        else:
            self.is_hover = False

    def draw(self, window):
        #Affichage pygame du pion
        if self.is_hover:
            window.blit(self.surface_hover, (self.x * 100 +6, self.y * 100 +6)) 
        else:
            window.blit(self.surface, (self.x * 100 +6, self.y * 100 +6)) 
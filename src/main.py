import pygame
from game import Game
from board import Board
from player import *

pygame.init()
game = Game(700,700)
game.run()
import pygame
from move import Move
from pawn import Pawn

class Board:


    def __init__(self, board_model):

        # Remplissage de la grille de jeu
        self.board = [[] ,[] ,[] ,[] ,[] ,[] ,[]]
        for i in range(7):
            for j in range(7):
                model = board_model[i][j]
                if model == 0:
                    self.board[i].append(None)
                if model == 1:
                    self.board[i].append(Pawn("black", i, j))
                if model == 2:
                    self.board[i].append(Pawn("white", i, j))
                if model == 3:
                    self.board[i].append(Pawn("king", i, j))
                

        self.background = pygame.image.load("images/background1.jpg") # Fond du plateau de jeu

        # Variables nécessaires à la gestion de la grille
        self.is_black_turn = True
        self.current_pawn = None
        self.has_king_escape = False
        self.ai_player = None

        

    def get_moves(self, pawn):
        #Renvoie tous les déplacements possibles du pion sous forme de liste de tuple
        coords = pawn.get_coord()

        x = coords[0]
        y = coords[1]
        while x > 0: # gauche
            x -= 1
            if self.board[x][y] == None:
                if ((x,y) == (0,0) or (x,y) == (0,6) or (x,y) == (6,0) or (x,y) == (6,6)) and pawn.team == "black" :  
                    
                    break
                else:
                    self.board[x][y] = Move(x,y)
            else:
                 break

        x = coords[0]
        y = coords[1]
        while x < 6: # droite
            x += 1
            if self.board[x][y] == None:
                if ((x,y) == (0,0) or (x,y) == (0,6) or (x,y) == (6,0) or (x,y) == (6,6)) and pawn.team == "black" :  
                    
                        break
                else:
                  self.board[x][y] = Move(x,y)
            else:
                  break

        x = coords[0]
        y = coords[1]
        while y > 0:  # haut
            y -= 1
            if self.board[x][y] == None:
                if ((x,y) == (0,0) or (x,y) == (0,6) or (x,y) == (6,0) or (x,y) == (6,6)) and pawn.team == "black" :  
                    break
                else:
                    self.board[x][y] = Move(x,y)
            else:
                  break

        x = coords[0]
        y = coords[1]
        while y < 6:  # bas
            y += 1
            if self.board[x][y] == None:
                if ((x,y) == (0,0) or (x,y) == (0,6) or (x,y) == (6,0) or (x,y) == (6,6)) and pawn.team == "black" :  
                    
                        break
                else:
                    self.board[x][y] = Move(x,y)
            else:
                  break



    def move(self, actual, goal):
        '''Bouge un pion des coordonnées actual aux coordonées goal'''
        
        if goal != (3,3) :
            obj = self.board[actual[0]][actual[1]]
            self.board[actual[0]][actual[1]] = None
            obj.set_coord(goal)
            obj.is_hover = False
            self.board[goal[0]][goal[1]] = obj
            self.is_black_turn = not self.is_black_turn
            return True
        else:
            if self.board[actual[0]][actual[1]].team == "black":
                return False
            else:
                obj = self.board[actual[0]][actual[1]]
                self.board[actual[0]][actual[1]] = None
                obj.set_coord(goal)
                obj.is_hover = False
                self.board[goal[0]][goal[1]] = obj
                self.is_black_turn = not self.is_black_turn
                return True

    def set_ai_player(self, ai_player):
        self.ai_player = ai_player

    def update_pawn(self, pawn):
        #le after d'un pion bougé
        coords = pawn.get_coord()

        if pawn.team == "black":
            opponents = ["white", "king"]
        else:
            opponents = ["black"]

        if pawn.team == "black":
            allies = ["black"]
        else:
            allies = ["white", "king"]

        # gauche
        x = coords[0]
        y = coords[1]
        if x-2 >= 0:
            if isinstance(self.board[x-1][y], Pawn) and self.board[x-1][y].team in opponents:
                if isinstance(self.board[x-2][y], Pawn) and self.board[x-2][y].team in allies:
                    self.board[x - 1][y] = None

        # droite
        x = coords[0]
        y = coords[1]
        if x + 2 <= 6:
            if isinstance(self.board[x + 1][y], Pawn) and self.board[x + 1][y].team in opponents:
                if isinstance(self.board[x + 2][y], Pawn) and self.board[x + 2][y].team in allies:
                    self.board[x + 1][y] = None

        # haut
        x = coords[0]
        y = coords[1]
        if y - 2 >= 0:
            if isinstance(self.board[x][y - 1], Pawn) and self.board[x][y - 1].team in opponents:
                if isinstance(self.board[x][y - 2], Pawn) and self.board[x][y - 2].team in allies:
                    self.board[x][y-1] = None

        # bas
        x = coords[0]
        y = coords[1]
        if y + 2 <= 6:
            if isinstance(self.board[x][y + 1], Pawn) and self.board[x][y + 1].team in opponents:
                if isinstance(self.board[x][y + 2], Pawn) and self.board[x][y + 2].team in allies:
                    self.board[x][y+1] = None
        
        if pawn.team == "king" and (coords == (0, 0) or coords == (0, 6) or coords == (6, 0) or coords == (6, 6)):
            return True
        return False


    def check_victory(self, has_king_escape):
        #on regarde si il y a une condition de victoire
        b = False
        k = False
        for line in self.board:
            for pawn in line:
                if isinstance(pawn, Pawn):
                    if pawn.team == "black":
                        b = True
                    if pawn.team == "king":
                        k = True
        if not b or self.has_king_escape:
            return 'w'
        if not k:
            return "b"
        else:
            return False

    def update(self, mouse):
        #misa a jour de la grille
        cliked = self.board[mouse[0]][mouse[1]]

        if isinstance(cliked, Move):
            is_moving = self.move(self.current_pawn.get_coord(), mouse)

            for line in range(7):
                for column in range(7):
                    if isinstance(self.board[line][column], Move):
                        self.board[line][column] = None

            if is_moving:
                self.has_king_escape = self.update_pawn(self.board[mouse[0]][mouse[1]])

        elif isinstance(cliked, Pawn):
            if (cliked.team == "black" and self.is_black_turn) or (cliked.team != "black" and not self.is_black_turn):
                self.current_pawn = cliked
                for line in range(7):
                    for column in range(7):
                        if isinstance(self.board[line][column], Move):
                            self.board[line][column] = None
                self.get_moves(self.current_pawn)

        else:
            self.current_pawn = None
            for line in range(7):
                for column in range(7):
                    if isinstance(self.board[line][column], Move):
                        self.board[line][column] = None

        status = self.check_victory(self.has_king_escape)
        return status

    def display(self, window, mouse):
        #Affichage du jeu
        
        window.blit(self.background, (0, 0))# la grille
        for i in range(1, 7):
            pygame.draw.rect(window, (0, 0, 0), (i * 100, 0, 2, 700))
        for i in range(1, 7):
            pygame.draw.rect(window, (0, 0, 0), (0, i * 100, 700, 2))

        
        for line in self.board:# le plateau
            for pawn in line:
                if pawn != None:
                    if isinstance(pawn, Pawn):
                        if (pawn.team == "black" and self.is_black_turn) or (pawn.team != "black" and not self.is_black_turn):
                            pawn.set_hover(mouse)
                    pawn.draw(window)
                    


    def get_best_move(self):
        best_move = None
        best_value = float('-inf')
        for pawn in self.get_all_pawns_for_team("white"):
            moves = self.get_moves(pawn)
            for move in moves:
                board_copy = self.copy_board()
                board_copy.move(pawn.get_coord(), move)
                value = self.evaluate_board(board_copy)
                if value > best_value:
                    best_move = (pawn.get_coord(), move)
                    best_value = value
        return best_move

 
import pygame
from pygame.locals import *


class AIPlayer:

    def __init__(self, color, human):
        self.color = color
        self.is_human = human #human est un booleen

        
    def make_move(self, board, depth, human_color):
        if self.is_human:
            while True:
                for event in pygame.event.get():
                    if event.type == MOUSEBUTTONDOWN:
                        position = self.get_mouse_position()
                        if board.is_valid_move(position, self.color):
                            return position
        else:
            position = self.get_best_move(board, depth, self.color, human_color)
            return position

   

    def move_ai(self):
        black_pawns = [pawn for row in self.board.board for pawn in row if isinstance(pawn, Pawn) and pawn.team == "black"]

    def get_best_move(self, board, depth, ai_color, human_color):
        def minimax_alpha_beta(board, depth, alpha, beta, maximizing_player):
            if depth == 0 or board.check_victory(board.has_king_escape):
                return None, self.evaluate(board)
            
            if maximizing_player:
                max_score = float('-inf')
                best_move = None
                
                for color in ["white", "black"]:
                    if color == ai_color:
                        pawn = self.get_pawn(color)
                    else:
                        pawn = self.get_pawn(human_color)
                        
                    for pawn in pawn:
                        for move in board.get_moves(pawn):
                            new_board = board.get_clone()
                            new_board.move(move, color)
                            _, score = minimax_alpha_beta(new_board, depth - 1, alpha, beta, False)
                            
                            if score > max_score:
                                max_score = score
                                best_move = move
                            
                            alpha = max(alpha, score)
                            if alpha >= beta:
                                break
                        else:
                            continue
                        break
                return best_move, max_score
            else:
                min_score = float('inf')
                best_move = None
                
                for color in ["white", "black"]:
                    if color == ai_color:
                        pawn = board.get_pawn(color)
                    else:
                        pawn = board.get_pawn(human_color)
                        
                    for pawn in pawn:
                        for move in board.get_moves(pawn):
                            new_board = board.get_clone()
                            new_board.move(move, color)
                            _, score = minimax_alpha_beta(new_board, depth - 1, alpha, beta, True)
                            
                            if score < min_score:
                                min_score = score
                                best_move = move
                            
                            beta = min(beta, score)
                            if alpha >= beta:
                                break
                        else:
                            continue
                        break
                return best_move, min_score
            
        return minimax_alpha_beta(board, depth, float('-inf'), float('inf'), True)[0]

    def evaluate(self, board):
        
        black_count = sum(1 for row in board.board for pawn in row if isinstance(pawn, Pawn) and pawn.team == "black")
        white_count = sum(1 for row in board.board for pawn in row if isinstance(pawn, Pawn) and pawn.team == "white")
        piece_count = black_count - white_count

        
        king_position = board.find_king("black")
        if king_position[0] == 0:
            king_score = 100
        elif king_position[0] == 1:
            king_score = 50
        else:
            king_score = 0

        
        black_moves = sum(len(board.get_moves(pawn)) for row in board.board for pawn in row if isinstance(pawn, Pawn) and pawn.team == "black")
        white_moves = sum(len(board.get_moves(pawn)) for row in board.board for pawn in row if isinstance(pawn, Pawn) and pawn.team == "white")
        move_count = black_moves - white_moves

      
        return piece_count * 10 + king_score + move_count



class HumanPlayer:

    def __init__(self, color):
        self.color = color
        self.is_human = True
        
    def get_mouse_position(self):
       #position de la souris
        x, y = pygame.mouse.get_pos()
        return (x, y)
        
    def make_move(self, board):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = self.get_mouse_position()
                    if board.is_valid_move(position, self.color):
                        return position

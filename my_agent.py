#!/usr/bin/env python3

"""
File Name:      my_agent.py
Authors:        Keshav Kolur and Anuj Bhyravabhotla
Date:           TODO: The date you finally started working on this.

Description:    Python file for my agent.
Source:         Adapted from recon-chess (https://pypi.org/project/reconchess/)
"""

import random
import chess
from player import Player


# TODO: Rename this class to what you would like your bot to be named during the game.
class MyAgent(Player):

    def __init__(self):
        pass
        
    def handle_game_start(self, color, board):
        """
        This function is called at the start of the game.

        :param color: chess.BLACK or chess.WHITE -- your color assignment for the game
        :param board: chess.Board -- initial board state
        :return:
        """
        # TODO: implement this method
        self.board = board
        self.color = color
        if color == chess.WHITE:
            self.board.set_fen("8/8/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        else:
            self.board.set_fen("rnbqkbnr/pppppppp/8/8/8/8/8/8 w KQkq - 0 1")
        # initialize trained model
        # initialize trained classifier
        
    def handle_opponent_move_result(self, captured_piece, captured_square):
        """
        This function is called at the start of your turn and gives you the chance to update your board.

        :param captured_piece: bool - true if your opponents captured your piece with their last move
        :param captured_square: chess.Square - position where your piece was captured
        """
        assert isinstance(self.board, chess.Board)
        if captured_piece:
             self.board.remove_piece_at(captured_square)
        self.board.turn = (self.color == chess.WHITE)
        pass

    def choose_sense(self, possible_sense, possible_moves, seconds_left):
        """
        This function is called to choose a square to perform a sense on.

        :param possible_sense: List(chess.SQUARES) -- list of squares to sense around
        :param possible_moves: List(chess.Moves) -- list of acceptable moves based on current board
        :param seconds_left: float -- seconds left in the game

        :return: chess.SQUARE -- the center of 3x3 section of the board you want to sense
        :example: choice = chess.A1
        """
        # TODO: update this method
        assert isinstance(possible_sense, list)
        i = 0
        while i < possible_sense.__len__():
            sense = possible_sense[i]
            if sense < 8 or sense > 55 or sense % 8 == 0 or (sense + 1) % 8 == 0:
                possible_sense.remove(sense)
            else:
                i += 1
        return random.choice(possible_sense)

    def handle_sense_result(self, sense_result):
        """
        This is a function called after your picked your 3x3 square to sense and gives you the chance to update your
        board.

        :param sense_result: A list of tuples, where each tuple contains a :class:`Square` in the sense, and if there
                             was a piece on the square, then the corresponding :class:`chess.Piece`, otherwise `None`.
        :example:
        [
            (A8, Piece(ROOK, BLACK)), (B8, Piece(KNIGHT, BLACK)), (C8, Piece(BISHOP, BLACK)),
            (A7, Piece(PAWN, BLACK)), (B7, Piece(PAWN, BLACK)), (C7, Piece(PAWN, BLACK)),
            (A6, None), (B6, None), (C8, None)
        ]
        """
        # TODO: implement this method
        # Hint: until this method is implemented, any senses you make will be lost.
        assert isinstance(self.board, chess.Board)
        for sense in sense_result:
            self.board.set_piece_at(sense[0], sense[1])


    def choose_move(self, possible_moves, seconds_left):
        """
        Choose a move to enact from a list of possible moves.

        :param possible_moves: List(chess.Moves) -- list of acceptable moves based only on pieces
        :param seconds_left: float -- seconds left to make a move
        
        :return: chess.Move -- object that includes the square you're moving from to the square you're moving to
        :example: choice = chess.Move(chess.F2, chess.F4)
        
        :condition: If you intend to move a pawn for promotion other than Queen, please specify the promotion parameter
        :example: choice = chess.Move(chess.G7, chess.G8, promotion=chess.KNIGHT) *default is Queen
        """
        # TODO: update this method
        assert isinstance(self.board, chess.Board)
        choice = random.choice(possible_moves)
        while not self.board.is_legal(choice):
            choice = random.choice(possible_moves)
        return choice
        
    def handle_move_result(self, requested_move, taken_move, reason, captured_piece, captured_square):
        """
        This is a function called at the end of your turn/after your move was made and gives you the chance to update
        your board.

        :param requested_move: chess.Move -- the move you intended to make
        :param taken_move: chess.Move -- the move that was actually made
        :param reason: String -- description of the result from trying to make requested_move
        :param captured_piece: bool - true if you captured your opponents piece
        :param captured_square: chess.Square - position where you captured the piece
        """
        # TODO: implement this method
        assert isinstance(self.board, chess.Board)
        if captured_piece:
            self.board.remove_piece_at(captured_square)
        self.board.push(taken_move if taken_move is not None else chess.Move.null())
        print(self.board)
        print(self.board.board_fen())
        pass
        
    def handle_game_end(self, winner_color, win_reason):  # possible GameHistory object...
        """
        This function is called at the end of the game to declare a winner.

        :param winner_color: Chess.BLACK/chess.WHITE -- the winning color
        :param win_reason: String -- the reason for the game ending
        """
        # TODO: implement this method
        pass


class StateEncoding():
    def __init__(self, color):
        self.color = color
        self.board = chess.Board()
        self.reward_map = {
            chess.PAWN: [
                0, 0, 0, 0, 0, 0, 0, 0,
                0.5, 1, 1, -2, -2, 1, 1, 0.5,
                0.5, -0.5, -1, 0, 0, -1, -0.5, 0.5,
                0, 0, 0, 2, 2, 0, 0, 0,
                0.5, 0.5, 1, 2.5, 2.5, 1, 0.5, 0.5,
                1, 1, 2, 3, 3, 2, 1, 1,
                5, 5, 5, 5, 5, 5, 5, 5,
                0, 0, 0, 0, 0, 0, 0, 0
            ],
            chess.KNIGHT: [
                -5, -4, -3, -3, -3, -3, -4, -5,
                -4, -2, 0, 0.5, 0.5, 0, -2, -4,
                -3, 0.5, 1, 1.5, 1.5, 1, 0.5, -3,
                -3, 0, 1.5, 2.0, 2.0, 1.5, 0, -3,
                -3, 0.5, 1.5, 2, 2, 1.5, 0.5, -3,
                -3, 0, 1, 1.5, 1.5, 1, 0, -3,
                -4, -2, 0, 0, 0, 0, -2, -4,
                -5, -4, -3, -3, -3, -3, -4, -5
            ],
            chess.BISHOP: [
                -2, -1, -1, -1, -1, -1, -1, -2,
                -1, 0.5, 0, 0, 0, 0, 0.5, -1,
                -1, 1, 1, 1, 1, 1, 1, -1,
                -1, 0, 1, 1, 1, 1, 0, -1,
                -1, 0.5, 0.5, 1, 1, 0.5, 0.5, -1,
                -1, 0, 0.5, 1, 1, 0.5, 0, -1,
                -1, 0, 0, 0, 0, 0, 0, -1,
                -2, -1, -1, -1, -1, -1, -1, -2
            ],
            chess.ROOK: [
                0, 0, 0, 0.5, 0.5, 0, 0, 0,
                -0.5, 0, 0, 0, 0, 0, 0, -0.5,
                -0.5, 0, 0, 0, 0, 0, 0, -0.5,
                -0.5, 0, 0, 0, 0, 0, 0, -0.5,
                -0.5, 0, 0, 0, 0, 0, 0, -0.5,
                -0.5, 0, 0, 0, 0, 0, 0, -0.5,
                0.5, 1, 1, 1, 1, 1, 1, 0.5,
                0, 0, 0, 0, 0, 0, 0, 0
            ],
            chess.QUEEN: [
                -2, -1, -1, -0.5, -0.5, -1, -1, -2,
                -1, 0, 0.5, 0, 0, 0, 0, -1,
                -1, 0.5, 0.5, 0.5, 0.5, 0.5, 0, -1,
                0, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5,
                -0.5, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5,
                -1, 0, 0.5, 0.5, 0.5, 0.5, 0, -1,
                -1, 0, 0, 0, 0, 0, 0, -1,
                -2, -1, -1, -0.5, -0.5, -1, -1, -2
            ],
            chess.KING: [
                2, 3, 1, 0, 0, 1, 3, 2,
                2, 2, 0, 0, 0, 0, 2, 2,
                -1, -2, -2, -2, -2, -2, -2, -1,
                -2, -3, -3, -4, -4, -3, -3, -2,
                -3, -4, -4, -5, -5, -4, -4, -3,
                -3, -4, -4, -5, -5, -4, -4, -3,
                -3, -4, -4, -5, -5, -4, -4, -3,
                -3, -4, -4, -5, -5, -4, -4, -3,
            ]
        }
        if not color:
            self.reward_map = {
                chess.PAWN: [
                    0, 0, 0, 0, 0, 0, 0, 0,
                    0.5, 1, 1, -2, -2, 1, 1, 0.5,
                    0.5, -0.5, -1, 0, 0, -1, -0.5, 0.5,
                    0, 0, 0, 2, 2, 0, 0, 0,
                    0.5, 0.5, 1, 2.5, 2.5, 1, 0.5, 0.5,
                    1, 1, 2, 3, 3, 2, 1, 1,
                    5, 5, 5, 5, 5, 5, 5, 5,
                    0, 0, 0, 0, 0, 0, 0, 0
                ].reverse(),
                chess.KNIGHT: [
                    -5, -4, -3, -3, -3, -3, -4, -5,
                    -4, -2, 0, 0.5, 0.5, 0, -2, -4,
                    -3, 0.5, 1, 1.5, 1.5, 1, 0.5, -3,
                    -3, 0, 1.5, 2.0, 2.0, 1.5, 0, -3,
                    -3, 0.5, 1.5, 2, 2, 1.5, 0.5, -3,
                    -3, 0, 1, 1.5, 1.5, 1, 0, -3,
                    -4, -2, 0, 0, 0, 0, -2, -4,
                    -5, -4, -3, -3, -3, -3, -4, -5
                ].reverse(),
                chess.BISHOP: [
                    -2, -1, -1, -1, -1, -1, -1, -2,
                    -1, 0.5, 0, 0, 0, 0, 0.5, -1,
                    -1, 1, 1, 1, 1, 1, 1, -1,
                    -1, 0, 1, 1, 1, 1, 0, -1,
                    -1, 0.5, 0.5, 1, 1, 0.5, 0.5, -1,
                    -1, 0, 0.5, 1, 1, 0.5, 0, -1,
                    -1, 0, 0, 0, 0, 0, 0, -1,
                    -2, -1, -1, -1, -1, -1, -1, -2
                ].reverse(),
                chess.ROOK: [
                    0, 0, 0, 0.5, 0.5, 0, 0, 0,
                    -0.5, 0, 0, 0, 0, 0, 0, -0.5,
                    -0.5, 0, 0, 0, 0, 0, 0, -0.5,
                    -0.5, 0, 0, 0, 0, 0, 0, -0.5,
                    -0.5, 0, 0, 0, 0, 0, 0, -0.5,
                    -0.5, 0, 0, 0, 0, 0, 0, -0.5,
                    0.5, 1, 1, 1, 1, 1, 1, 0.5,
                    0, 0, 0, 0, 0, 0, 0, 0
                ].reverse(),
                chess.QUEEN: [
                    -2, -1, -1, -0.5, -0.5, -1, -1, -2,
                    -1, 0, 0.5, 0, 0, 0, 0, -1,
                    -1, 0.5, 0.5, 0.5, 0.5, 0.5, 0, -1,
                    0, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5,
                    -0.5, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5,
                    -1, 0, 0.5, 0.5, 0.5, 0.5, 0, -1,
                    -1, 0, 0, 0, 0, 0, 0, -1,
                    -2, -1, -1, -0.5, -0.5, -1, -1, -2
                ].reverse(),
                chess.KING: [
                    2, 3, 1, 0, 0, 1, 3, 2,
                    2, 2, 0, 0, 0, 0, 2, 2,
                    -1, -2, -2, -2, -2, -2, -2, -1,
                    -2, -3, -3, -4, -4, -3, -3, -2,
                    -3, -4, -4, -5, -5, -4, -4, -3,
                    -3, -4, -4, -5, -5, -4, -4, -3,
                    -3, -4, -4, -5, -5, -4, -4, -3,
                    -3, -4, -4, -5, -5, -4, -4, -3,
                ].reverse()
            }
        self.material_differential = 0
        self.dists = [
            [True, 0, 0, 0, 1, 0, 0], [True, 0, 1, 0, 0, 0, 0], [True, 0, 0, 1, 0, 0, 0], [True, 0, 0, 0, 0, 1, 0],
            [True, 0, 0, 0, 0, 0, 1], [True, 0, 0, 1, 0, 0, 0], [True, 0, 1, 0, 0, 0, 0], [True, 0, 0, 0, 1, 0, 0],
            [True, 1, 0, 0, 0, 0, 0], [True, 1, 0, 0, 0, 0, 0], [True, 1, 0, 0, 0, 0, 0], [True, 1, 0, 0, 0, 0, 0],
            [True, 1, 0, 0, 0, 0, 0], [True, 1, 0, 0, 0, 0, 0], [True, 1, 0, 0, 0, 0, 0], [True, 1, 0, 0, 0, 0, 0],
            [],[],[],[],[],[],[],[],
            [],[],[],[],[],[],[],[],
            [],[],[],[],[],[],[],[],
            [],[],[],[],[],[],[],[],
            [False, 1, 0, 0, 0, 0, 0], [False, 1, 0, 0, 0, 0, 0], [False, 1, 0, 0, 0, 0, 0], [False, 1, 0, 0, 0, 0, 0],
            [False, 1, 0, 0, 0, 0, 0], [False, 1, 0, 0, 0, 0, 0], [False, 1, 0, 0, 0, 0, 0], [False, 1, 0, 0, 0, 0, 0]
            [False, 0, 0, 0, 1, 0, 0], [False, 0, 1, 0, 0, 0, 0], [False, 0, 0, 1, 0, 0, 0], [False, 0, 0, 0, 0, 1, 0],
            [False, 0, 0, 0, 0, 0, 1], [False, 0, 0, 1, 0, 0, 0], [False, 0, 1, 0, 0, 0, 0], [False, 0, 0, 0, 1, 0, 0],
        ]

    def set_probability(self, color, square, piece, value):
        self.dists[square][piece] = value
        self.dists[square][0] = color

    def set_possible_moves(self, possible_moves):
        self.possible_moves = possible_moves

    def believe_square_is_empty(self, square):
        self.dists[square].clear()

    def update_board(self):
        assert isinstance(self.board, chess.Board)
        for square_index in range(64):
            square = self.dists[square_index]
            arr_len = square.__len__()
            color = False
            piece = None
            if arr_len > 0:
                color = square[0]
                piece = 1
                max_prob = -1
                for x in range(1, arr_len):
                    if max_prob < square[x]:
                        max_prob = square[x]
                        piece = x
            if piece is None:
                self.board.remove_piece_at(square_index)
            else:
                self.board.set_piece_at(square_index, chess.Piece(piece, color))

    def compute_reward(self):
        reward = self.material_differential



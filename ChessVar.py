# Author: Walter Jeffries
# GitHub username: treylingo1
# Date: 05/23/2023
# Description: Chess class that allows for a fully functionable game of chess

class ChessVar:
    """
    ChessVar class
    """
    def __init__(self):
        """
        Initialize the ChessVar object, setting up the board, turn, game state,
        and dictionaries to track captured pieces and piece counts.
        """
        self._board = self._initialize_board()
        self._player_turn = 'white'
        self._game_state = 'UNFINISHED'
        self._captured_pieces = {'white': {'p': 0, 'r': 0, 'n': 0, 'b': 0, 'q': 0, 'k': 0},
                                 'black': {'p': 0, 'r': 0, 'n': 0, 'b': 0, 'q': 0, 'k': 0}}
        self._piece_counts = {'white': {'p': 8, 'r': 2, 'n': 2, 'b': 2, 'q': 1, 'k': 1},
                              'black': {'p': 8, 'r': 2, 'n': 2, 'b': 2, 'q': 1, 'k': 1}}

    def _initialize_board(self):
        """
        Initialize the chess board with the starting positions of the pieces.
        """
        board = [
                 ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
                 ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                 ['.', '.', '.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.', '.', '.'],
                 ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                 ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
                 ]
        return board

    def print_board(self):
        """
        Prints the current state of the board with row and column labels.
        """
        print("  a b c d e f g h")
        for i, row in enumerate(self._board):
            print(8 - i, end=" ")
            print(" ".join([piece if piece != "." else '.' for piece in row]), end=" ")
            print(8 - i)
        print("  a b c d e f g h")

    def get_game_state(self):
        """
        Get the current game state.
        """
        return self._game_state

    def _is_within_board(self, row, col):
        """
        Check if the given row and column are within the bounds of the board.
        """
        return 0 <= row < 8 and 0 <= col < 8

    def _pos_to_indices(self, pos):
        """
        Convert a position in algebraic notation to board indices.
        """
        column, row = pos
        return 8 - int(row), ord(column) - ord('a')

    def _indices_to_pos(self, indices):
        """
        Convert board indices to a position in algebraic notation.
        """
        row, col = indices
        return chr(col + ord('a')) + str(8 - row)

    def make_move(self, from_pos, to_pos):
        """
        Attempt to make a move from one position to another.
        """

        #Checks to make sure the game is unfinished
        if self._game_state != 'UNFINISHED':
            return False

        from_row, from_col = self._pos_to_indices(from_pos)
        to_row, to_col = self._pos_to_indices(to_pos)

        #Making sure the move that's going to be performed is within the board
        if not self._is_within_board(from_row, from_col) or not self._is_within_board(to_row, to_col):
            return False

        piece = self._board[from_row][from_col]
        target_piece = self._board[to_row][to_col]

        #Checking to make sure the move being performed isn't in the spot of a empty space, or that the attempted move
        # isn't being made for the wrong piece(ex: white player is trying to move a black piece
        if piece == '.' or (piece.isupper() and self._player_turn != 'white') or (piece.islower() and self._player_turn != 'black'):
            return False

        if target_piece != '.' and (
                (piece.isupper() and target_piece.isupper()) or (piece.islower() and target_piece.islower())):
            return False

        if not self._is_valid_move(piece, from_pos, to_pos):
            return False

        captured_piece = self._board[to_row][to_col]


        # Check if the move results in both kings being captured
        if self._would_both_kings_be_captured(piece, captured_piece):
            return False

        if captured_piece != '.':
            self._explode_pieces(to_row, to_col)
            self._board[to_row][to_col] = '.'
            self._board[from_row][from_col] = '.'
            self._capture_piece(piece)

        else:
            self._board[to_row][to_col] = piece
            self._board[from_row][from_col] = '.'

        # Check for game state after the move
        if self._check_win():
            return True

        #Changes the turn of the player after a move is performed
        self._player_turn = 'black' if self._player_turn == 'white' else 'white'
        return True

    def _is_valid_move(self, piece, from_pos, to_pos):
        """
        Determines if a move is valid for a given piece.
        """
        from_row, from_col = self._pos_to_indices(from_pos)
        to_row, to_col = self._pos_to_indices(to_pos)
        delta_row = to_row - from_row
        delta_col = to_col - from_col
        target_piece = self._board[to_row][to_col]

        if piece.lower() == 'p':
            if piece.isupper():
                if from_row == 6 and delta_row == -2 and delta_col == 0 and target_piece == '.':
                    return True
                if delta_row == -1 and delta_col == 0 and target_piece == '.':
                    return True
                if delta_row == -1 and abs(delta_col) == 1 and target_piece != '.' and target_piece.islower():
                    return True
            else:
                if from_row == 1 and delta_row == 2 and delta_col == 0 and target_piece == '.':
                    return True
                if delta_row == 1 and delta_col == 0 and target_piece == '.':
                    return True
                if delta_row == 1 and abs(delta_col) == 1 and target_piece != '.' and target_piece.isupper():
                    return True
        if piece.lower() == 'r':
            if (from_row == to_row or from_col == to_col) and self._path_clear(from_pos, to_pos):
                return True
        if piece.lower() == 'n':
            if (abs(delta_row), abs(delta_col)) in [(2, 1), (1, 2)]:
                return True
        if piece.lower() == 'b':
            if abs(delta_row) == abs(delta_col):
                return self._path_clear(from_pos, to_pos)
        if piece.lower() == 'q':
            if from_row == to_row or from_col == to_col or abs(delta_row) == abs(delta_col):
                return self._path_clear(from_pos, to_pos)
        if piece.lower() == 'k':
            if max(abs(delta_row), abs(delta_col)) == 1:
                return True
        return False

    def _path_clear(self, from_pos, to_pos):
        """
        Check if the path between two positions is clear (no pieces blocking).
        """
        from_row, from_col = self._pos_to_indices(from_pos)
        to_row, to_col = self._pos_to_indices(to_pos)
        delta_row = to_row - from_row
        delta_col = to_col - from_col
        step_row = (delta_row > 0) - (delta_row < 0)
        step_col = (delta_col > 0) - (delta_col < 0)
        cur_row, cur_col = from_row + step_row, from_col + step_col
        while (cur_row, cur_col) != (to_row, to_col):
            if self._board[cur_row][cur_col] != '.':
                return False
            cur_row += step_row
            cur_col += step_col
        return True

    def _explode_pieces(self, row, col):
        """
        Handle the explosion of pieces in a 3x3 area centered on the given position, excluding kings.
        """
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if 0 <= r < 8 and 0 <= c < 8:
                    piece = self._board[r][c]
                    if piece != '.' and piece.lower() != 'p':
                        if piece.lower() == 'k':
                            self._game_state = 'WHITE_WON' if piece == 'k' else 'BLACK_WON'
                        self._board[r][c] = '.'

    def _capture_piece(self, piece):
        """
        Capture a piece and update the captured pieces and piece counts.
        """
        color = 'white' if piece.isupper() else 'black'
        piece = piece.lower()
        self._captured_pieces[color][piece] += 1
        self._piece_counts[color][piece] -= 1

    def _check_win(self):
        """
        Check if the game has been won by capturing a king.
        """
        if self._piece_counts['white']['k'] == 0:
            self._game_state = 'BLACK_WON'
            return True
        if self._piece_counts['black']['k'] == 0:
            self._game_state = 'WHITE_WON'
            return True
        return False

    def _would_both_kings_be_captured(self, piece, captured_piece):
        """
        Check if a move would result in both kings being captured.
        """
        if piece.lower() == 'k' and captured_piece.lower() == 'k':
            return True
        return False

    def _is_in_checkmate(self):
        """
        Check if the current player is in checkmate.
        """
        king_pos = None
        for r in range(8):
            for c in range(8):
                if (self._player_turn == 'white' and self._board[r][c] == 'K') or \
                        (self._player_turn == 'black' and self._board[r][c] == 'k'):
                    king_pos = (r, c)
                    break
            if king_pos:
                break

        if not king_pos:
            return False

        for r in range(8):
            for c in range(8):
                if (self._player_turn == 'white' and self._board[r][c].islower()) or \
                        (self._player_turn == 'black' and self._board[r][c].isupper()):
                    if self._is_valid_move(self._board[r][c], self._indices_to_pos((r, c)),
                                           self._indices_to_pos(king_pos)):
                        return True
        return False

    def _is_in_stalemate(self):
        """
        Check if the game is in stalemate.
        """
        for r in range(8):
            for c in range(8):
                if (self._player_turn == 'white' and self._board[r][c].isupper()) or \
                        (self._player_turn == 'black' and self._board[r][c].islower()):
                    for nr in range(8):
                        for nc in range(8):
                            if self._is_valid_move(self._board[r][c], self._indices_to_pos((r, c)),
                                                   self._indices_to_pos((nr, nc))):
                                return False
        return True

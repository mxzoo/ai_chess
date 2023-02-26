import Piece

def parse_fen(fen_string):
    #Done: parses a FEN string into a piece array to be passed into the Board constructor
    #To-do: some invalid FEN strings (e.g. too many pieces/empty spaces for a rank) are still considered valid
    legal_chars = ["p", "r", "n", "b", "q", "k", "P", "R", "N", "B", "Q", "K", "1", "2", "3", "4", "5", "6", "7", "8", "/"]
    piece_name_map = {
        "P" : "Pawn",
        "R" : "Rook",
        "N" : "Knight",
        "B" : "Bishop",
        "Q" : "Queen",
        "K" : "King"
    }
    ranks = ["8", "7", "6", "5", "4", "3", "2", "1"]
    files = ["a", "b", "c", "d", "e", "f", "g", "h"]
    rank_counter = 0
    file_counter = 0

    piece_array = []

    for i in fen_string:
        if i not in legal_chars:
            #To-do: invalid FEN string error
            return
        elif i.isnumeric():
            file_counter += int(i)
        elif i == "/":
            rank_counter += 1
            file_counter = 0
        else:
            type = i
            name = piece_name_map[i.upper()]
            is_white = i.isupper()
            position = files[file_counter] + ranks[rank_counter]
            coords = [file_counter, rank_counter]
            new_piece = Piece.Piece(type, name, is_white, position, coords)
            piece_array.append(new_piece)
            file_counter += 1
        
    return piece_array

def square_in_direction(direction, coords, spaces):
    #Done: given a set of starting coords, returns the square z spaces in a given direction
    if direction == "north-west":
        return [coords[0]-spaces, coords[1]-spaces]
    elif direction == "north":
        return [coords[0], coords[1]-spaces]
    elif direction == "north-east":
        return [coords[0]+spaces, coords[1]-spaces]
    elif direction == "east":
        return [coords[0]+spaces, coords[1]]
    elif direction == "south-east":
        return [coords[0]+spaces, coords[1]+spaces]
    elif direction == "south":
        return [coords[0], coords[1]+spaces]
    elif direction == "south-west":
        return [coords[0]-spaces, coords[1]+spaces]
    elif direction == "west":
        return [coords[0]-spaces, coords[1]]
    return None

class Board:

    def __init__(self, pieces) -> None:
        self.pieces = pieces

    def check_valid_square(self, coords):
        #Check if input square is valid (exists on the board)
        for i in range(2):
            if coords[i] < 0 or coords[i] > 7:
                return False
        return True

    def check_empty_square(self, coords):
        #Check if input square is empty
        for piece in self.pieces:
            if piece.coords == coords:
                return False
        return True

    def piece_at(self, coords):
        for piece in self.pieces:
            if piece.coords == coords:
                return piece
        return None

    def calculate_semi_legal_moves(self, coords):
        #Done: given the current coords of a piece on the board, calculate all semi-legal moves it can make (disregards pins and checks)
        selected_piece = None
        possible_moves = []

        for piece in self.pieces:
            if piece.coords == coords:
                selected_piece = piece
                starting_coords = piece.coords
        
        if selected_piece.name == "Pawn":
            #Done: implemented move logic for first move + diagonal takes
            #To-do: en passant not implemented, rewrite code to increase readability/reduce lines
            if selected_piece.is_white:
                if not selected_piece.has_moved:
                    if self.check_valid_square(square_in_direction("north", starting_coords, 2))\
                    and self.check_empty_square(square_in_direction("north", starting_coords, 2)):
                        possible_moves.append(square_in_direction("north", starting_coords, 2))
                if self.check_valid_square(square_in_direction("north", starting_coords, 1))\
                and self.check_empty_square(square_in_direction("north", starting_coords, 1)):
                    possible_moves.append(square_in_direction("north", starting_coords, 1))
                sides = [square_in_direction("north-west", starting_coords, 1), square_in_direction("north-east", starting_coords, 1)]
                for side in sides:
                    if self.check_valid_square(side)\
                    and not self.check_empty_square(side) and not self.piece_at(side).is_white:
                        possible_moves.append(side)
            if not selected_piece.is_white:
                if not selected_piece.has_moved:
                    if self.check_valid_square(square_in_direction("south", starting_coords, 2))\
                    and self.check_empty_square(square_in_direction("south", starting_coords, 2)):
                        possible_moves.append(square_in_direction("south", starting_coords, 2))
                if self.check_valid_square(square_in_direction("south", starting_coords, 1))\
                and self.check_empty_square(square_in_direction("south", starting_coords, 1)):
                    possible_moves.append(square_in_direction("south", starting_coords, 1))
                sides = [square_in_direction("south-west", starting_coords, 1), square_in_direction("south-east", starting_coords, 1)]
                for side in sides:
                    if self.check_valid_square(side)\
                    and not self.check_empty_square(side) and self.piece_at(side).is_white:
                        possible_moves.append(side)

        elif selected_piece.name == "Rook":
            #Done: move horizontally and vertically along an axis, take enemy pieces and stop, blocked by ally pieces
            moves_in_direction = {
                "north" : True,
                "east" : True,
                "south" : True,
                "west" : True,
            }
            
            for direction in moves_in_direction.keys():
                counter = 1
                while moves_in_direction[direction]:
                    square = square_in_direction(direction, starting_coords, counter)
                    if not self.check_valid_square(square):
                        moves_in_direction[direction] = False
                    elif not self.check_empty_square(square):
                        if self.piece_at(square).is_white == selected_piece.is_white:
                            moves_in_direction[direction] = False
                        elif moves_in_direction[direction]:
                            possible_moves.append(square)
                            moves_in_direction[direction] = False
                    elif self.check_empty_square(square) and moves_in_direction[direction]:
                        possible_moves.append(square)
                    counter += 1
                
        elif selected_piece.name == "Knight":
            #Done: all knight moves, captures and ally blocks
            knight_moves = [
                [starting_coords[0]-1, starting_coords[1]-2], [starting_coords[0]+1, starting_coords[1]-2],
                [starting_coords[0]+2, starting_coords[1]-1], [starting_coords[0]+2, starting_coords[1]+1],
                [starting_coords[0]+1, starting_coords[1]+2], [starting_coords[0]-1, starting_coords[1]+2],
                [starting_coords[0]-2, starting_coords[1]+1], [starting_coords[0]-2, starting_coords[1]-1]
            ]
            for move in knight_moves:
                if self.check_valid_square(move) and \
                (self.check_empty_square(move) or (self.piece_at(move).is_white != selected_piece.is_white)):
                    possible_moves.append(move)

        elif selected_piece.name == "Bishop":
            #Done: diagonal movement, captures and ally blocks
            moves_in_direction = {
                "north-west" : True,
                "north-east" : True,
                "south-east" : True,
                "south-west" : True,
            }

            for direction in moves_in_direction.keys():
                counter = 1
                while moves_in_direction[direction]:
                    square = square_in_direction(direction, starting_coords, counter)
                    if not self.check_valid_square(square):
                        moves_in_direction[direction] = False
                    elif not self.check_empty_square(square):
                        if self.piece_at(square).is_white == selected_piece.is_white:
                            moves_in_direction[direction] = False
                        elif moves_in_direction[direction]:
                            possible_moves.append(square)
                            moves_in_direction[direction] = False
                    elif self.check_empty_square(square) and moves_in_direction[direction]:
                        possible_moves.append(square)
                    counter += 1

        elif selected_piece.name == "Queen":
            #Done: all movement, captures and ally blocks
            moves_in_direction = {
                "north-west" : True,
                "north" : True,
                "north-east" : True,
                "east" : True,
                "south-east" : True,
                "south" : True,
                "south-west" : True,
                "west" : True,
            }

            for direction in moves_in_direction.keys():
                counter = 1
                while moves_in_direction[direction]:
                    square = square_in_direction(direction, starting_coords, counter)
                    if not self.check_valid_square(square):
                        moves_in_direction[direction] = False
                    elif not self.check_empty_square(square):
                        if self.piece_at(square).is_white == selected_piece.is_white:
                            moves_in_direction[direction] = False
                        elif moves_in_direction[direction]:
                            possible_moves.append(square)
                            moves_in_direction[direction] = False
                    elif self.check_empty_square(square) and moves_in_direction[direction]:
                        possible_moves.append(square)
                    counter += 1 

        elif selected_piece.name == "King":
            #Done: all king moves, captures and ally blocks
            #To-do: castles
            king_moves = [
                [starting_coords[0]-1, starting_coords[1]-1], [starting_coords[0], starting_coords[1]-1],
                [starting_coords[0]+1, starting_coords[1]-1], [starting_coords[0]+1, starting_coords[1]],
                [starting_coords[0]+1, starting_coords[1]+1], [starting_coords[0], starting_coords[1]+1],
                [starting_coords[0]-1, starting_coords[1]+1], [starting_coords[0]-1, starting_coords[1]],
            ]
            for move in king_moves:
                if self.check_valid_square(move) and \
                (self.check_empty_square(move) or (self.piece_at(move).is_white != selected_piece.is_white)):
                    possible_moves.append(move)

            if selected_piece.has_moved == False:
                #To-do: check the kings rank for pieces
                for piece in self.pieces:
                    if piece.name == "Rook" and piece.is_white == selected_piece.is_white and piece.has_moved == False:
                        if piece.coords[0] == 0:
                            pass
                        elif piece.coords[0] == 7:
                            pass

                         

        return possible_moves

    def check_piece_pinned(self, coords):
        #Done: check whether the piece at the given coords is pinned
        pinning_pieces = ["Rook", "Bishop", "Queen"]
        selected_piece = self.piece_at(coords)
        first_check_counter = 0
        second_check_counter = 0

        for piece in self.pieces:
            if piece.is_white == selected_piece.is_white and piece.name == "King":
                ally_king = piece

        for piece in self.pieces:
            if piece.is_white != selected_piece.is_white and piece.name in pinning_pieces:
                if ally_king.coords in self.calculate_semi_legal_moves(piece.coords):
                    first_check_counter += 1
        
        selected_piece.coords = None

        for piece in self.pieces:
            if piece.is_white == selected_piece.is_white and piece.name == "King":
                ally_king = piece
        for piece in self.pieces:
            if piece.is_white != selected_piece.is_white and piece.name in pinning_pieces:
                if ally_king.coords in self.calculate_semi_legal_moves(piece.coords):
                    second_check_counter += 1
        
        selected_piece.coords = coords
        if second_check_counter > first_check_counter:
            return True
        return False

    def calculate_legal_moves(self, coords):
        #Done: given the current coords of a piece on the board, calculate most legal moves (accounting for pins, checks)
        #To-do: implement castles and en passants
        legal_moves = []
        selected_piece = self.piece_at(coords)
        
        #Done: check for checks on the king
        attackers = []
        check_counter = 0
        for piece in self.pieces:
            if piece.is_white == selected_piece.is_white and piece.name == "King":
                ally_king = piece
        for piece in self.pieces:
            if piece.is_white != selected_piece.is_white:
                if ally_king.coords in self.calculate_semi_legal_moves(piece.coords):
                    attackers.append(piece)
                    check_counter += 1
        
        if selected_piece != ally_king and check_counter > 1:
            #Done: double or more checks are unblockable -> only king moves allowed
            return []
        elif selected_piece != ally_king and check_counter == 1:
            #Done: if piece is pinned and king is checked, only king moves allowed
            if self.check_piece_pinned(coords):
                return []
            #Done: calculate blocks/captures
            attacker = attackers[0]
            if attacker.name == "Pawn":
                #Done: pawn attacks cannot be blocked, only captured
                if attacker.coords in self.calculate_semi_legal_moves(selected_piece.coords):
                    return [attacker.coords]
                return []
            if attacker.name == "Knight":
                #Done: knight attacks are unblockable, only captures allowed
                if attacker.coords in self.calculate_semi_legal_moves(selected_piece.coords):
                    return [attacker.coords]
                return []
            elif attacker.name == "Bishop":
                #Done: bishop attacks can be blocked or captured
                blocking_squares = []
                blocking_squares.append(attacker.coords)
                if attacker.coords[0] < ally_king.coords[0] and attacker.coords[1] < ally_king.coords[1]:
                    for i in range(ally_king.coords[0] - attacker.coords[0]):
                        blocking_squares.append(square_in_direction("south-east", attacker.coords, i))
                elif attacker.coords[0] < ally_king.coords[0] and attacker.coords[1] > ally_king.coords[1]:
                    for i in range(ally_king.coords[0] - attacker.coords[0]):
                        blocking_squares.append(square_in_direction("south-west", attacker.coords, i))
                elif attacker.coords[0] > ally_king.coords[0] and attacker.coords[1] > ally_king.coords[1]:
                    for i in range(attacker.coords[0] - ally_king.coords[0]):
                        blocking_squares.append(square_in_direction("north-west", attacker.coords, i))
                elif attacker.coords[0] > ally_king.coords[0] and attacker.coords[1] < ally_king.coords[1]:
                    for i in range(attacker.coords[0] - ally_king.coords[0]):
                        blocking_squares.append(square_in_direction("north-east", attacker.coords, i))
                legal_moves = []
                for move in self.calculate_semi_legal_moves(selected_piece.coords):
                    if move in blocking_squares:
                        legal_moves.append(move)
                return legal_moves
            elif attacker.name == "Rook":
                #Done: rook attacks can be blocked or captured
                blocking_squares = []
                blocking_squares.append(attacker.coords)
                if attacker.coords[0] == ally_king.coords[0] and attacker.coords[1] < ally_king.coords[1]:
                    for i in range(ally_king.coords[1] - attacker.coords[1]):
                        blocking_squares.append(square_in_direction("south", attacker.coords, i))
                elif attacker.coords[0] == ally_king.coords[0] and attacker.coords[1] > ally_king.coords[1]:
                    for i in range(attacker.coords[1] - ally_king.coords[1]):
                        blocking_squares.append(square_in_direction("north", attacker.coords, i))
                elif attacker.coords[0] < ally_king.coords[0] and attacker.coords[1] == ally_king.coords[1]:
                    for i in range(ally_king.coords[0] - attacker.coords[0]):
                        blocking_squares.append(square_in_direction("west", attacker.coords, i))
                elif attacker.coords[0] > ally_king.coords[0] and attacker.coords[1] == ally_king.coords[1]:
                    for i in range(attacker.coords[0] - ally_king.coords[0]):
                        blocking_squares.append(square_in_direction("east", attacker.coords, i))
                legal_moves = []
                for move in self.calculate_semi_legal_moves(selected_piece.coords):
                    if move in blocking_squares:
                        legal_moves.append(move)
                return legal_moves
            elif attacker.name == "Queen":
                #Done: queen attacks can be blocked or captured
                blocking_squares = []
                blocking_squares.append(attacker.coords)
                if attacker.coords[0] < ally_king.coords[0] and attacker.coords[1] < ally_king.coords[1]:
                    for i in range(ally_king.coords[0] - attacker.coords[0]):
                        blocking_squares.append(square_in_direction("south-east", attacker.coords, i))
                elif attacker.coords[0] < ally_king.coords[0] and attacker.coords[1] > ally_king.coords[1]:
                    for i in range(ally_king.coords[0] - attacker.coords[0]):
                        blocking_squares.append(square_in_direction("south-west", attacker.coords, i))
                elif attacker.coords[0] > ally_king.coords[0] and attacker.coords[1] > ally_king.coords[1]:
                    for i in range(attacker.coords[0] - ally_king.coords[0]):
                        blocking_squares.append(square_in_direction("north-west", attacker.coords, i))
                elif attacker.coords[0] > ally_king.coords[0] and attacker.coords[1] < ally_king.coords[1]:
                    for i in range(attacker.coords[0] - ally_king.coords[0]):
                        blocking_squares.append(square_in_direction("north-east", attacker.coords, i))
                elif attacker.coords[0] == ally_king.coords[0] and attacker.coords[1] < ally_king.coords[1]:
                    for i in range(ally_king.coords[1] - attacker.coords[1]):
                        blocking_squares.append(square_in_direction("south", attacker.coords, i))
                elif attacker.coords[0] == ally_king.coords[0] and attacker.coords[1] > ally_king.coords[1]:
                    for i in range(attacker.coords[1] - ally_king.coords[1]):
                        blocking_squares.append(square_in_direction("north", attacker.coords, i))
                elif attacker.coords[0] < ally_king.coords[0] and attacker.coords[1] == ally_king.coords[1]:
                    for i in range(ally_king.coords[0] - attacker.coords[0]):
                        blocking_squares.append(square_in_direction("west", attacker.coords, i))
                elif attacker.coords[0] > ally_king.coords[0] and attacker.coords[1] == ally_king.coords[1]:
                    for i in range(attacker.coords[0] - ally_king.coords[0]):
                        blocking_squares.append(square_in_direction("east", attacker.coords, i))
                legal_moves = []
                for move in self.calculate_semi_legal_moves(selected_piece.coords):
                    if move in blocking_squares:
                        legal_moves.append(move)
                return legal_moves

        elif selected_piece != ally_king and check_counter == 0:
            #Done: check for pins
            if self.check_piece_pinned(coords):
                #Done: the pinning piece can either be taken or blocked
                selected_piece.coords = None
                legal_moves = []
                for piece in self.pieces:
                    if piece.is_white != selected_piece.is_white and ally_king.coords in self.calculate_semi_legal_moves(piece.coords):
                        pinner = piece
                if pinner is not None:
                    blocking_squares = []
                    blocking_squares.append(pinner.coords)
                    blocking_squares.append(self.calculate_semi_legal_moves.pinner)
                    for move in self.calculate_semi_legal_moves(selected_piece):
                        if move in blocking_squares:
                            legal_moves.append(move)
                return legal_moves
            else:
                #Done: non-pinned pieces can move wherever when king is not checked
                return self.calculate_semi_legal_moves(coords)

        elif selected_piece == ally_king and check_counter > 0:
            #Done: return all king moves - ones covered by attackers
            legal_moves = self.calculate_semi_legal_moves(coords)
            for piece in self.pieces:
                if piece.is_white != ally_king.is_white:
                    for square in self.calculate_semi_legal_moves(piece.coords):
                        if square in legal_moves:
                            legal_moves.remove(square)
            return legal_moves

    def move_piece(self, start_coords, end_coords):
        #Done: given the current position of a piece on the board, move it to the desired (legal) position
        #To-do: implement castle and en passant functionalities
        piece = self.piece_at(start_coords)
        
        if self.piece_at(end_coords) != None:
            self.pieces.remove(self.piece_at(end_coords))
        
        piece.coords = end_coords
        piece.has_moved = True
    
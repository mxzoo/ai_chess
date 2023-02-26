import os
import pygame as pg

import Board
import Piece

piece_clicked = False
clicked_coords = None
move_coords = None

#Tester method - returns textual respresentation on pieces on the board
def piece_array_to_text(piece_array):
    for piece in piece_array:
        type = piece.type
        name = piece.name
        is_white = piece.is_white
        position = piece.position

        print(type, name, is_white, position)

def get_clicked_coords(pos):
    for x in range(8):
        for y in range(8):
            if x*100 <= pos[0] < (x+1)*100 and y*100 <= pos[1] < (y+1)*100:
                return [x, y]

def screen_update(screen, board, pieces_img):
    squares = pg.Surface((100*8, 100*8))
    squares.fill((255, 233, 197))

    for x in range(1, 8, 2):
        for y in range(0, 7, 2):
            pg.draw.rect(squares, (150, 104, 64), (x*100, y*100, 100, 100))
    for x in range(0, 7, 2):
        for y in range(1, 8, 2):
            pg.draw.rect(squares, (150, 104, 64), (x*100, y*100, 100, 100))

    if piece_clicked == True:
        legal_moves = board.calculate_legal_moves(clicked_coords)
        for move in legal_moves:
            pg.draw.rect(squares, [100, 100, 100], (move[0]*100, move[1]*100, 100, 100))
    
    screen.blit(squares, squares.get_rect())

    for piece in board.pieces:
        piece_coords = [piece.coords[0]*100, piece.coords[1]*100]
        screen.blit(pieces_img[piece.type], piece_coords)

if __name__ == "__main__":
    #To do
    pieces = Board.parse_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
    board = Board.Board(pieces)

    screen = pg.display.set_mode((800, 800))

    pg.init()

    pieces_img = {
        "p" : pg.image.load(os.path.join("img", "b_pawn.svg")),
        "r" : pg.image.load(os.path.join("img", "b_rook.svg")),
        "n" : pg.image.load(os.path.join("img", "b_knight.svg")),
        "b" : pg.image.load(os.path.join("img", "b_bishop.svg")),
        "q" : pg.image.load(os.path.join("img", "b_queen.svg")),
        "k" : pg.image.load(os.path.join("img", "b_king.svg")),
        "P" : pg.image.load(os.path.join("img", "w_pawn.svg")),
        "R" : pg.image.load(os.path.join("img", "w_rook.svg")),
        "N" : pg.image.load(os.path.join("img", "w_knight.svg")),
        "B" : pg.image.load(os.path.join("img", "w_bishop.svg")),
        "Q" : pg.image.load(os.path.join("img", "w_queen.svg")),
        "K" : pg.image.load(os.path.join("img", "w_king.svg")),
    }

    for piece in pieces_img:
        pieces_img[piece] = pg.transform.scale(pieces_img[piece], (100, 100))

    run = True
    while run:
        screen_update(screen, board, pieces_img)
        pg.display.update()
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                pos = pg.mouse.get_pos()
                old_clicked_coords = clicked_coords
                clicked_coords = get_clicked_coords(pos)
                if piece_clicked == True and clicked_coords in move_coords:
                    board.move_piece(old_clicked_coords, clicked_coords)
                    piece_clicked = False
                elif board.piece_at(get_clicked_coords(pos)) != None:
                    piece_clicked = True
                    move_coords = board.calculate_legal_moves(clicked_coords)
                else:
                    piece_clicked = False
                    clicked_coords = None
                    move_coords = None

            if event.type == pg.MOUSEBUTTONUP and event.button == 3:
                piece_clicked = False
                clicked_coords = None